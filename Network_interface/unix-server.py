import socket
import os
import time


SERVER_PATH = "/tmp/unix-server.py"

def run_server():
    if os.path.exists(SERVER_PATH):
        os.remove(SERVER_PATH)

    print "Starting unix domain socket server"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_PATH)
    server.listen(5)

    print "Listening on path: %s" % SERVER_PATH

    while True:
        conn, addr = server.accept()
        datagram = conn.recv(1024)
        if not datagram:
            break
        else:
            print "-" * 20
            print datagram
            conn.sendall(datagram)
        if "DONE" == datagram:
            break
    print "-" * 20
    print "Server is shutting down now .. "
    server.close()
    os.remove(SERVER_PATH)
    print "Server shutdown and path removed"

if __name__ == "__main__':
    run_server()
