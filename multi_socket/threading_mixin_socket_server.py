import os
import socket
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024


def client(ip, port , message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall((message).encode())
        response = sock.recv(BUF_SIZE)
        print ("Client received: %s" % response)
    finally:
        sock.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_thread = threading.current_thread()
        response = '%s : %s' % (current_thread.name, data)
        print ("server sending response [current_thread name: data] = %s" %
                response)
        self.request.send((response).encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT),
            ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print ('Server loop running thread: %s' % server_thread.name)

    client(ip, port , "Hello from client1")
    client(ip, port , "Hello from client2")
    client(ip, port , "Hello from client3")

    server.shutdown()

if __name__ == "__main__":
    main()
