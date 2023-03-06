from socket import *

IP = '0.0.0.0'
TAG_PORT = 5000
UI_PORT = 10000
BUFLEN = 512
TRACK_COMMAND = 'track'
STOP_COMMAND = 'stop'
PARK_COMMAND = 'park'
mode = STOP_COMMAND


# The socket to receive coordinates from the tag
tagSocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
# The socket to receive commands from the UI
UISocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
UISocket.settimeout(5)
# The socket to send information to the turtlebot
tbSocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
# The 

tagSocket.bind((IP,TAG_PORT))

print(f'The sever is start, waiting to connect at port {TAG_PORT}')


while True:
    #-----Receive data from one raspberry pi (The coordinates)-----
    received, addr = tagSocket.recvfrom(BUFLEN)
    if not received:
        break
    coordinates = received.decode()
    print(f'Recieved the coordinates: {coordinates}')
    #-----Receive data from the UI raspberry pi(Commands)----
    try:
        received2, addr = UISocket.recvfrom(BUFLEN)
        mode = received2.decode()['command']
        destination = received2.decode['coordinates']
    except(timeout):
        pass

    # Send the coordinates to the turtle bot under the tracking mode
    if(mode == TRACK_COMMAND):
        print(coordinates)
    
    # Tell the turtlebot to stop under the STOP mode
    #elif(mode == STOP_COMMAND):
        
    # Tell the turtlebot to go to the parking point
    #elif(mode == PARK_COMMAND):


    
tagSocket.close()


