from socket import *
import commands

class CommandSocket:

  

  def __init__(self, ip, port = 50001):
    self.ip=ip
    self.port=port
    self.dataSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    self.dataSocket.connect((self.ip, self.port))
    self.BUFLEN = 1024
  
  def sendCommand(self, toSend): 
    self.dataSocket.send(toSend.encode())
    recved = self.dataSocket.recv(self.BUFLEN)
    print(recved.decode())
    
  def close(self):
    self.dataSocket.close()
