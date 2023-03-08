from socket import *

IP = '0.0.0.0'

PORT = 50000

BUFLEN = 512

listenSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)

listenSocket.bind((IP,PORT))

listenSocket.listen()
print(f'The sever is start, waiting to connect at port {PORT}')

dataSocket, addr = listenSocket.accept()
print('Accept a client to connect:', addr)

while True:
    recved = dataSocket.recv(BUFLEN)

    if not recved:
        break
    
    info = recved.decode()
    print(f'Recieved the information: {info}')

    dataSocket.send(f'The server received the information {info}'.encode())
    
dataSocket.close()
listenSocket.close()
