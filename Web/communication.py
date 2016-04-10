__author__ = 'Claude'
import socket


def communicate(data, ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(str(data))
        response = sock.recv(1024)
        sock.close()
        return eval(response)
    except:
        return None