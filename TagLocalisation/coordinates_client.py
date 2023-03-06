#Client running on pi@jolteon
#Receives coordinates from UWB module through serial usb communication
#Sends coordinates to DICE machine server
import serial
import time
import datetime
import json
from socket import *

#socket parameters
IP = "129.215.2.45" #change to IP of DICE machine server
SERVER_PORT = 40000
BUFLEN = 256

#initialise socket
dataSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

#connect to serial port of UWB sensor
DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
print("Connected to " + DWM.name)

#send 2 Enters to start sensor's shell mode
DWM.write("\r\r".encode())
print("Encode")
time.sleep(1)

#send command lec to start receiving measurements
DWM.write("lec\r".encode())
print("Encode")

time.sleep(1)
try:
    while True:
        #attempt to read sensor reading.
        data = DWM.readline().decode()
        if(data):
            #print(data)
            #print(type(data))
            if ("DIST" in data and "AN0" in data and "AN1" in data and "AN2" in data):
                data = data.replace("\r\n", "")
                data = data.split(",")
                if("DIST" in data):
                    anchor_Number = int(data[data.index("DIST")+1])
                    for i in range(anchor_Number):
                        pos_AN = {"id": data[data.index("AN"+str(i))+1], "x": data[data.index("AN"+str(i))+2], "y": data[data.index(
                            "AN"+str(i))+3], "dist": data[data.index("AN"+str(i))+5]}
                        pos_AN = json.dumps(pos_AN)
                        #print(pos_AN)
                        #r.set('AN'+str(i), pos_AN)
                if("POS" in data):
                    pos = {"x": data[data.index("POS")+1],
                           "y": data[data.index("POS")+2]}
                    pos = json.dumps(pos)
                    print(pos)
                    #send coordinates to server
                    toSend = pos
                    dataSocket.sendto(toSend.encode(), (IP, SERVER_PORT))
                    #received = dataSocket.recvfrom(BUFLEN)
    #DWM.write("\r".encode())
    #DWM.close()
    #dataSocket.close()

except KeyboardInterrupt:
    DWM.write("\r".encode())
    DWM.close()
    dataSocket.close()
    print("Stop")
