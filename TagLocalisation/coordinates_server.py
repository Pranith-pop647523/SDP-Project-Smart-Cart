from socket import *
import sys

IP = '0.0.0.0'
TAG_PORT = 5000
UI_PORT = 10000
TURTLEBOT_IP = ''
TURTLEBOT_PORT = 15000
BUFLEN = 512
TRACK = 2
STOP = 1
PARK = 3
mode = TRACK

#----Use the following code if you want to input these arguments from the console
#TAG_PORT = sys.argv[1]
#UI_PORT = sys.argv[2]
#TURTLEBOT_IP = sys.argv[3]
#TURTLEBOT_PORT = sys.argv[4]

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
        mode = received2.decode()
    except(timeout):
        pass

    # Send the coordinates to the turtle bot under the tracking mode
    if(mode == TRACK):
        #tbSocket.sendto(coordinates,(TURTLEBOT_IP,TURTLEBOT_PORT))
        print(coordinates)

    
    # Tell the turtlebot to stop under the STOP mode
    #elif(mode == STOP):
        tbSocket.sendto()
        
    # Tell the turtlebot to go to the parking point
    #elif(mode == PARK):


    
tagSocket.close()


