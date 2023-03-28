import serial
import time
import json

class SerialClient:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serialClient = None
        
    def connect(self):
        try:
            self.serialClient = serial.Serial(self.port, self.baudrate)
            self.name = self.serialClient.name
        except:
            return False
        return True
        
    def enterShellMode(self):
        #send 2 Enters to start sensor's shell mode
        self.serialClient.write("\r\r".encode())
        time.sleep(1)

        #send command 'lec' to start receiving sensor measurements
        self.serialClient.write("lec\r".encode())
        time.sleep(1)
    
    def readData(self):
        data = self.serialClient.readline().decode()
        if (data):
            if ("DIST" in data and "AN0" in data and "AN1" in data and "AN2" in data):
                data = data.replace("\r\n", "")
                data = data.split(",")

                if("DIST" in data):
                    anchor_Number = int(data[data.index("DIST")+1])
                    for i in range(anchor_Number):
                        pos_AN = {"id": data[data.index("AN"+str(i))+1],
                                    "x": data[data.index("AN"+str(i))+2],
                                    "y": data[data.index("AN"+str(i))+3],
                                    "dist": data[data.index("AN"+str(i))+5]}
                        pos_AN = json.dumps(pos_AN) #convert to python dictionary
                #get x and y coordinates from data 
                if("POS" in data):
                    pos = {"x": data[data.index("POS")+1],
                           "y": data[data.index("POS")+2]}
                    pos = json.dumps(pos)
                    return pos
        return None
        
    def close(self):
        if (self.serialClient):
            self.serialClient.write("\r".encode())
            self.serialClient.close()
