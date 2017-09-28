import argparse
import sys
import socket
import fcntl
import struct
import array


SIOCGIFADDR = 0x8915

def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK.DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), SIOCGIFADDR,
        struct.pack('256s', ifname[:15]))[20:24])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(decription = 'Python Networking Utils')
    parser.add_argument('--ifname', action='store', dest = 'ifname',
            required=True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    print ("Interface [%s] --> IP: %s" % (ifname, get_ip(ifname))
