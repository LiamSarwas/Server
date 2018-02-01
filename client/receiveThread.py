import sys
import socket
import threading
import time
import os
import config

from clntUser import User


class receiveThread (threading.Thread):
    def __init__(self, clientPort):
	threading.Thread.__init__(self)
	self.clientPort = clientPort

    def run(self):
	listen(self.clientPort)

def receive(conn, address):
    while 1:
	received = ''
	data = conn.recv(1024)
        received += data
	if(len(data) < 1024):
	    break
	
    messages = received.split(',')
    messages[0] = int(messages[0])
    messages[1] = int(messages[1])
    #define the behaviour for recieving messages of all kinds here
    
    #if message is just an incoming message
    if(messages[0] == 1):
	usermess = messages[2].split(' ')
	user = usermess[0]
	mess = ''
	for i in range(1, len(usermess)):
	    mess = mess + usermess[i] + ' '
	print('{} says: {}'.format(user, mess))
	return 1

    #if message is a logout message
    if(messages[0] == 2):
	print(messages[2])
	os._exit(1)
	return 1

    if(messages[0] == 3):
	print(messages[2])
	return 1
    
    #used to set up the userList
    if(messages[0] == 4):
	users = messages[2].split(' ')
	for user in users:
	    config.users.userList.append(User(user, -1, -1))
	return 1


def listen(clientPort):
    HOST = ''
    PORT = clientPort
    clientListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientListener.bind((HOST, PORT))
    while True:
	clientListener.listen(1)
	conn, address = clientListener.accept()
	while 1:
	    output = receive(conn, address)
	    if(output == 1):
	    	break
