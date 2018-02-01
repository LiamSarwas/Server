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

def authenticate():
    user = raw_input('username: ')
    password = raw_input('password: ')
    userpass = user + ' ' + password
    return userpass

class loginThread (threading.Thread):
    def __init__(self, serverHostname, serverPort, clientPort):
	threading.Thread.__init__(self)
	self.serverHostname = serverHostname
	self.serverPort = serverPort
	self.clientPort = clientPort

    def run(self):
	loginMain(self.serverHostname, self.serverPort, self.clientPort)

def loginMain(serverHostname, serverPort, clientPort):
    clntSocket = connectToServer(serverHostname, serverPort)
    userpass = authenticate()
    send = userpass + ' ' + str(clientPort)
    output = message(0, send)
    clntSocket.sendall(output.message)
    while 1:
	while 1:
	    received = ''
	    data = clntSocket.recv(1024)
	    received += data
	    if(len(data) < 1024):
		break
	    
	messages = received.split(',')
	messages[0] = int(messages[0])
	messages[1] = int(messages[1])
	if(messages[0] == 2):
	    break
	print(messages[2])
	userpass = authenticate()
	send = userpass + ' ' + str(clientPort)
	output = message(0, send)
	clntSocket.sendall(output.message)

    user = userpass.split(' ')
    config.currentUser = user[0]
    print(messages[2])
    print('Type help to get started.')
    clntSocket.close()
