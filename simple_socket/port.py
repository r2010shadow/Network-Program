import socket

def port_name():
    protocolname = 'tcp'
    for port in [80,25]:
        print "Port: %s => service name : %s " % (port, socket.getservbyport
                (port, protocolname))

    print "Port: %s => service name : %s " % (53,
                socket.getservbyport(port,protocolname))

if __name__ == "__main__":
    port_name()
