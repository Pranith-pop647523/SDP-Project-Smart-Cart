from socket import *
from socket_server import *

IP = '0.0.0.0'

TAG_PORT = 50000
UI_PORT = 50001
BUFLEN = 512
STOP = '1'
FOLLOW = '2'
PARK = '3'
mode = FOLLOW

#start coordinates server:
coordinatesSocket = SocketServer(IP, TAG_PORT, 0.1, 512) 
print(f'Server started, waiting for tag at port {TAG_PORT}.')

#start ui commands server:
commandsSocket = SocketServer(IP, UI_PORT, 0.1, 512)
print(f'Waiting for UI at port {UI_PORT}.')

#connect to coordinates client:
addr = coordinatesSocket.accept()
print('Connected to coordinates client:', addr)

#connect to ui client:
addr = commandsSocket.accept()
print('Connected to ui client:', addr)

#main loop:
try: 
    while True:
    	#receive command before timeout:
        command = commandsSocket.receive() #returns None if timeout
        #if a command is received, update mode.
        if (command != None):
            mode = command
            if(mode == STOP):
                print('STOP')
            elif(mode == FOLLOW):
                print('FOLLOW')
            elif(mode == PARK):
                print('PARK')

        #receve coordinates from tag
        tagData = coordinatesSocket.receive() #returns None if timeout
        if (tagData != None):
            coordinates = tagData
            print(f'Received coordinates: {coordinates}')
        
        if (mode == FOLLOW):
            print('Follow mode')
            #publish ros goal
    
        elif mode == STOP:
            print('Stop command')
            #cancel ros goal
    
        elif (mode == PARK):
            print('Park command')
            #call parking routine

except KeyboardInterrupt:
    commandsSocket.close()
    coordinatesSocket.close()
