import socket
import sys, os
import time
import threading
import config

from message import message

def connectToServer(host, port): 
    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try:
    	clntSocket.connect((host, port))
    except socket.error, (value, label):
	print('Connection to server could not be resolved: ' + label)
	os._exit(1)
    return clntSocket

class heartbeatThread (threading.Thread):
    def __init__(self, delay, hostname, port):
	threading.Thread.__init__(self)
	self.delay = delay
	self.hostname = hostname
	self.port = port

    def run(self):
	heartbeatMain(self.hostname, self.port, self.delay)
	
def heartbeatMain(hostname, port, delay):
    while True:
	time.sleep(delay)
	clntSocket = connectToServer(hostname, port)
	#send the heartbeat message to server
	heartbeat = message(8, config.currentUser)
	clntSocket.send(heartbeat.message)
