from socket import *

IP = '0.0.0.0'

TAG_PORT = 50000
UI_PORT = 50001
BUFLEN = 512
STOP = '1'
FOLLOW = '2'
PARK = '3'
mode = FOLLOW

#start coordinates server:
tagListenSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
tagListenSocket.bind((IP,TAG_PORT))
tagListenSocket.listen()
print(f'Server started, waiting for tag at port {TAG_PORT}.')

#start ui commands server:
uiListenSocket = socket(AF_INET,SOCK_STREAM, IPPROTO_TCP)
uiListenSocket.bind((IP,UI_PORT))
uiListenSocket.listen()
print(f'Waiting for UI at port {UI_PORT}.')

#connect to coordinates client:
tagDataSocket, addr = tagListenSocket.accept()
tagDataSocket.settimeout(0.1)
print('Connected to coordinates client:', addr)

#connect to ui client:
uiDataSocket, addr = uiListenSocket.accept()
uiDataSocket.settimeout(0.1)
print('Connected to ui client:', addr)

#main loop:
while True:
    try:
    	#receive command before timeout:
        command = uiDataSocket.recv(BUFLEN)
        #if a command is received, update mode.
        mode = command.decode()
        uiDataSocket.send(f'The server received the information {mode}'.encode())
        if(mode == STOP):
            print('STOP')
        elif(mode == FOLLOW):
            print('FOLLOW')
        elif(mode == PARK):
            print('PARK')
    except timeout:
        pass


    try:
        receivedTag = tagDataSocket.recv(BUFLEN)
        coordinates = receivedTag.decode()
        tagDataSocket.send(f'The server received the information {coordinates}'.encode())
        
        print(f'Received coordinates: {coordinates}')
    except timeout:
        pass
        
        
    
    if (mode == FOLLOW):
        #print coordinates
        #print(f'Recieved coordinates: {info}')
        print('Follow mode')
    
        
        


    elif mode == STOP:
        print('Stop command')

    
tagDataSocket.close()
tagListenSocket.close()
uiDataSocket.close()
uiListenSocket.close()
