#!/usr/bin/python3

import serial
import time
import datetime
import json
from socket import *
import sys
import subprocess
import daemon
from daemon import pidfile
import logging
import os
import signal
from socket_client import *
from serial_client import *
import lockfile

#TCP parameters
SERVER_IP = '129.215.3.153' #IP address of DICE machine / server
SERVER_PORT = 50000
BUFLEN = 512

#Serial Port parameters
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 115200


class CoordinatesClient:
    
    def __init__(self, pidfile):
        try:
            os.remove(pidfile)
        except:
            pass
        try:
            os.remove(pidfile + ".lock")
        except:
            pass
        self.pidfile = pidfile
        self.running = False
        print("initialised")
    
    def start(self):
        if self.running:
            print("Daemon already running.")
            return
        
        #write pid into pidfile
        with open(self.pidfile, 'w') as f:
            f.write(str(os.getpid()))
	
        print("wrote")
        self.context = daemon.DaemonContext (
            pidfile=lockfile.FileLock(self.pidfile),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        self.context.signal_map = {
            signal.SIGTERM: self.stop
        }
        print("try to open")
        self.context.open()
        self.running = True
        print("startRoutine")
        self.startRoutine()
        
    def stop(self, *a):
        self.logger.info("Termination signal received.")
        if not self.running:
            print("Daemon not running.")
            return
        #self.close()
        #with open(self.pidfile, 'r') as f:
        #    pid = int(f.read())
        #os.kill(pid, signal.SIGTERM)
        #os.remove(self.pidfile)
        self.running = False
        self.serialClient.close()
        self.socketClient.close()
        os.remove(pidfile)
        self.logger.info("Process closed gracefully")
        sys.exit(0)
        
    def startLogger(self):
        self.logger = logging.getLogger('coordinates_client')
        self.logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler('/home/pi/smart_cart/coordinates_client.log')
        fh.setLevel(logging.INFO)
        
        formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formatstr)
        
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.info("Process coordinates_client started")
        
    def connectSocket(self):
        socketConnected = False
        while (not socketConnected and self.running):
            self.logger.info("Connecting to server at " + SERVER_IP + "...")
            socketConnected = self.socketClient.connect()
            time.sleep(1)
        if (socketConnected):
            self.logger.info("Connected to server.")
    
    def connectSerial(self):
    
        serialConnected = False
        while (not serialConnected and self.running):
            self.logger.info("Connecting to serial port " + SERIAL_PORT + "...")
            serialConnected = self.serialClient.connect()
            time.sleep(1)
        if (serialConnected):
            self.logger.info("Connected to serial port.")
            
    def startRoutine(self):
        #create logger
        self.startLogger()
        
        #initialise  TCP socket
        self.socketClient = SocketClient(SERVER_IP, SERVER_PORT, BUFLEN)
        #initialise serial port
        self.serialClient = SerialClient(SERIAL_PORT, BAUDRATE)
        
        #connect to TCP socket
        self.connectSocket()
        #connect to serial port of UWB sensor
        self.connectSerial()
        
        if (self.running):
            self.serialClient.enterShellMode()
        
        while (self.running):
            #attempt to read sensor reading
            coordinates = self.serialClient.readData()
            if (not coordinates is None):
                self.logger.info("Sent coordinates to server")
                reply = self.socketClient.sendData(coordinates)
                if (reply):
                    self.logger.info("Server replied: " + reply)
                else:
                    self.logger.info("Server did not reply")
        #self.close()
        #self.logger.info("program closed gracefully")
        #os.remove(pidfile)
        #sys.exit(0)

    #def close(self):
    #    self.serialClient.close()
    #    self.socketClient.close()

def signal_handler(signal, frame):
    #print("signal1")
    #thisDaemon.logger.info("received termination signal.")
    #print("signal2")
    #thisDaemon.logger.info("test")
    thisDaemon.stop()

pidfile = '/home/pi/smart_cart/coordinates_client.pid'
thisDaemon = CoordinatesClient(pidfile)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


thisDaemon.start()
#if len(sys.argv) > 1:
#    if sys.argv[1] == 'start':
#        thisDaemon.start()
#    elif sys.argv[1] == 'stop':
#        thisDaemon.stop()
#    else:
#        print(f"Unknown command: {sys.argv[1]}")
#        sys.exit(1)
#else:
#    print(f"Usage: {sys.argv[0]} start|stop")
#    sys.exit(1)
