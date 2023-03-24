from socket import *

class SocketServer:

    def __init__(self, ip, port, timeout = 0.1, buflen = 512):
        self.listenSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
        self.listenSocket.bind((ip, port))
        self.listenSocket.listen()
        self.timeout = timeout
        self.buflen = buflen
        
    def accept(self):
        accepted = False
        while (not accepted):
            try:
                self.connection, addr = self.listenSocket.accept()
                self.connection.settimeout(self.timeout)
                accepted = True
                return addr
            except:
                pass
        return
        
    def receive(self):
        try:
            data = self.connection.recv(self.buflen).decode()
            self.connection.send(f'Received the information {data}'.encode())
            return data
        except timeout:
            return None
        
            
    def close(self):
        self.connection.close()
        self.listenSocket.close()
    