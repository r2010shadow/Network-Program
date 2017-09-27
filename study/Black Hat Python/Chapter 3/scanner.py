#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 活动主机扫描器

import socket
import os
import struct
import threading

from netaddr import IPNetwork,IPAddress
from ctypes import *

# Host to listen on
host   = "192.168.1.222"

# Subnet to target
subnet = "192.168.1.0/24"

# Magic we'll check ICMP responses for
magic_message = "PYTHONRULES!"

def udp_sender(subnet,magic_message):
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message,("%s" % ip, 65212))
        except:
            pass

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        # ("src", c_ulong),
        # ("dst", c_ulong)
        ("src", c_uint32),
        ("dst", c_uint32)
    ]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        # Map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        
        # Human readable IP addresses
        # self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        # self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
        # '@I' is unisigned int in native order, because c_ulong is 4 bytes in i386 and 8 in amd64.
        # struct.calcsize('@BBHHHBBHLL') is 20 in i386 and 32 in amd64 which is size of _fields_.
        # In actual it's 28 bytes in amd64 plus 4 bytes padded for word alignment.
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))
    
        # Human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

# Create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP 
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# We want the IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# If we're on Windows we need to send some ioctls to setup promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# Start sending packets
t = threading.Thread(target=udp_sender,args=(subnet, magic_message))
t.start()        

try:
    while True:
        # Read in a single packet
        # IP paket size is (2^16) - 1
        raw_buffer = sniffer.recvfrom(65535)[0]
        
        # Create an IP header from the first 20 bytes of the buffer
        # ip_header = IP(raw_buffer[0:20])    # For x86
        # ip_header = IP(raw_buffer[0:32])    # For amd64
        ip_header = IP(raw_buffer)    # For all
      
        # print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)
    
        # If it's ICMP we want it
        if ip_header.protocol == "ICMP":
            # Calculate where our ICMP packet starts
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            
            # Create our ICMP structure
            icmp_header = ICMP(buf)
            
            # print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)

            # Now check for the TYPE 3 and CODE 3 which indicates a host is up but no port available to talk to
            if icmp_header.code == 3 and icmp_header.type == 3:
                # Check to make sure we are receiving the response that lands in our subnet
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    # Test for our magic message
                    if raw_buffer[len(raw_buffer)-len(magic_message):] == magic_message:
                        print "Host Up: %s" % ip_header.src_address
# Handle CTRL-C
except KeyboardInterrupt:
    # If we're on Windows turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)