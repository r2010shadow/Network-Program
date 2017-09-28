import argparse
import socket
import fcntl
import struct
import nmap


SAMPLE_PORT = '21-23'
SIOCGIFADDR = 0x8915

def get_interface_status(name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', name[:15]))[20-24]
    nm = nmap.PortScanner()
    nm.scan(ip_address, SAMPLE_PORT)
    print (nm[ip_address])
    return nm[ip_address].state()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Python')
    parser.add_argument('-name', action='store', dest='name', required=True)
    given_args = parser.parse_args()
    name=given_args.name
    print "Interface [%s] --> IP:%s" % (name, get_interface_status(name))

