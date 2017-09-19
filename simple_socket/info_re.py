import socket

'''
    remote host info shower

'''


def info_re():
    remote_host = 'www.python.org'
    try:
        print ("IP addr: %s" % socket.gethostbyname(remote_host))
    except socket.error, err_msg:
        print("%s: %s" % (remote_host, err_msg))


if __name__ == "__main__":
    info_re()
