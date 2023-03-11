#Client running on pi@jolteon
#Receives coordinates from UWB module through serial usb communication
#Sends coordinates to DICE machine server
import serial
import time
import datetime
import json
from socket import *

#TCP parameters
IP = '129.215.2.45' #IP address of DICE machine / server
SERVER_PORT = 50000
BUFLEN = 1024

#create TCP socket
dataSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
dataSocket.connect((IP,SERVER_PORT))
#connect to serial port of UWB sensor
DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
print("Connected to " + DWM.name)

#send 2 Enters to start sensor's shell mode
DWM.write("\r\r".encode())
print("Encode")
time.sleep(1)

#send command 'lec' to start receiving sensor measurements
DWM.write("lec\r".encode())
print("Encode")

time.sleep(1)

#loop reads serial data and sends them to TCP socket
try:
    while True:
        #attempt to read sensor reading.
        data = DWM.readline().decode()
        if(data):
            if ("DIST" in data and "AN0" in data and "AN1" in data and "AN2" in data):
                data = data.replace("\r\n", "")
                data = data.split(",")

                if("DIST" in data):
                    anchor_Number = int(data[data.index("DIST")+1])
                    for i in range(anchor_Number):
                        pos_AN = {"id": data[data.index("AN"+str(i))+1], "x": data[data.index("AN"+str(i))+2], "y": data[data.index("AN"+str(i))+3], "dist": data[data.index("AN"+str(i))+5]}
                        pos_AN = json.dumps(pos_AN)
                #get x and y coordinates from data 
                if("POS" in data):
                    pos = {"x": data[data.index("POS")+1],
                           "y": data[data.index("POS")+2]}
                    pos = json.dumps(pos)
                    print(pos)
                    #send coordinates to server
                    toSend = pos
                    dataSocket.send(toSend.encode())
                    #wait for reply
                    recved = dataSocket.recv(BUFLEN)
                    
                    if not recved:
                        break

                    print(recved.decode())
                    
except KeyboardInterrupt:
    DWM.write("\r".encode())
    DWM.close()
    dataSocket.close()
    print("Stop")

