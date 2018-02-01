import socket
import sys, os
import time
import threading
import config

def connectToServer(host, port): 
    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    	clntSocket.connect((host, port))
    except socket.error, (value, label):
	print('Connection to server could not be resolved: ' + label)
    	os._exit(1)
    return clntSocket

class clientThread (threading.Thread):
    def __init__(self, hostname, port, send):
	threading.Thread.__init__(self)
	self.hostname = hostname
	self.port = port
	self.send = send

    def run(self):
	clientMain(self.hostname, self.port, self.send)

def receive(conn):
    while 1:
	received = ''
	data = conn.recv(1024)
	received += data
	if(len(data) < 1024):
	    break
    
    messages = received.split(',')
    messages[0] = int(messages[0])
    messages[1] = int(messages[1])

    if(messages[0] == -1):
	print(messages[2])
	return 1
    if(messages[0] == 1):
	#message was good but dont print
	return 1
    if(messages[0] == 2):
	#message was good and print
	print(messages[2])
	return 1
    if(messages[0] == 3):
	#message was return of a getaddress request
	useripport = messages[2].split(' ')
	for user in config.users:
	    if(user.username == useripport[0]):
		user.ip_address = useripport[1]
		user.port = useripport[2]
		if(str(user.ip_address) == '-1' and int(user.port) == -1):
		    print('That user is not currently logged in.')
	return 1
	
def clientMain(hostname, port, send):
    clntSocket = connectToServer(hostname, port)
    clntSocket.sendall(send.message)
    while 1:
	output = receive(clntSocket)
	if(output == 1):
	    break	
    clntSocket.close()
