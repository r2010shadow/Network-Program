import os
import socket
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkingClient():
    def __init__(self, ip , port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print ('PID %s sending echo message to the server:  %s' %
                (current_process_id, ECHO_MSG))
        send_data_length = self.sock.send((ECHO_MSG).encode())  #for py3 str
        print ('Sent: %d characters, so far .. ' % send_data_length)
        response = self.sock.recv(BUF_SIZE)
        print ('PID %s received: %s' % (current_process_id, response[5:]))

    def shutdown(self):
        self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = '%s: %s' % (current_process_id, data)
        print ("server sending response [current_process_id: data] = %s" %
                response)
        self.request.send((response).encode())  #for py3 send add .encode()
        return

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST,SERVER_PORT),
            ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print ('Server loop running PID: %s' % os.getpid())

    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()

#bug.   sometimes  can not shutdonw by itself .
