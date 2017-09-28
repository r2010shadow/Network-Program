import socket
import sys

SERVER_PATH = "/tmp/unix-server"

def run_client():
    socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    server_address = SERVER_PATH

    print "Connecting to %s" % server_address
    try:
        sock.connect(server_address)
    except socket.error, msg:
        print >> sys.stderr, msg
        sys.exit(1)

    try:
        message = "This is the message. this will be echoed back"
        print "Sending [%s] " % message
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_excepted:
            data = sock.recv(16)
            amount_received += len(data)
            print >> sys.stdout, "Received [%s] " % data
    finally:
        print "Closing client"
        sock.close()

if __name__ == "__main__":
    run_client()
