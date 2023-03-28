import socket
from socket import *

class SocketClient:
    def __init__(self, ip, port, buflen = 512):
        self.ip = ip
        self.port = port
        self.buflen = buflen
        self.dataSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
    
    def connect(self):
        try:
            self.dataSocket.connect((self.ip, self.port))
        except:
            return False
        return True

    def sendData(self, data):
        recved = None
        self.dataSocket.send(data.encode())
        #wait for reply
        try:
            recved = self.dataSocket.recv(self.buflen)
        except:
            pass
        if recved:
            recved = recved.decode()
        return recved

    def close(self):
        self.dataSocket.close()
