#!/usr/bin/env python
import socket

'''
    Local host info shower.
    1. hostname
    2. IP

'''


def print_info_lo():
    host_name = socket.gethostname()
    ip_addr = socket.gethostbyname(host_name)
    print ("host name: %s" % host_name)
    print ("IP addr: %s " % ip_addr)

if __name__ == "__main__":
    print_info_lo()
