from socket import *

IP = '0.0.0.0'

TAG_PORT = 50000
UI_PORT = 50001
BUFLEN = 512
STOP = '1'
FOLLOW = '2'
PARK = '3'
mode = FOLLOW

tagListenSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
tagListenSocket.bind((IP,TAG_PORT))
tagListenSocket.listen()
print(f'The sever is start, waiting for tag to connect at port {TAG_PORT}')

uiListenSocket = socket(AF_INET,SOCK_STREAM, IPPROTO_TCP)
uiListenSocket.bind((IP,UI_PORT))
uiListenSocket.listen()
print(f'The sever is start, waiting for UI to connect at port {UI_PORT}')



tagDataSocket, addr = tagListenSocket.accept()
print('Accept a tag client to connect:', addr)

uiDataSocket, addr = uiListenSocket.accept()
uiDataSocket.settimeout(5)
print('Accept a UI client to connect:', addr)
while True:
    try:
        command = uiDataSocket.recv(BUFLEN)
        mode = command.decode()
    except timeout:
        pass

    if mode == FOLLOW:
        receivedTag = tagDataSocket.recv(BUFLEN)
    
    
        if not receivedTag:
            break
    
        info = receivedTag.decode()
        print(f'Recieved the information: {info}')

        tagDataSocket.send(f'The server received the information {info}'.encode())

    elif mode == STOP:
        print('Stop command')

    
tagDataSocket.close()
tagListenSocket.close()
uiDataSocket.close()
uiListenSocket.close()
