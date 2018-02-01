import socket
import sys, os
import time
import threading
import config
from message import message

class ServerHeartbeatThread (threading.Thread):
    def __init__(self, delay):
	threading.Thread.__init__(self)
	self.delay = delay

    def run(self):
	heartbeatMain(self.delay)

def heartbeatMain(delay):
    while True:
	time.sleep(delay)
	for user in config.users:
	    if(user.logged_in == True):
		print(user.username + ' ' + str(user.seen))
		print(user.username + ' ' + str(user.not_seen))
		if(user.seen == True):
		    user.seen = False
		    user.not_seen = 0
		elif(user.seen == False and user.not_seen <= 2):
		    user.seen == False
		    user.not_seen = user.not_seen + 1
		else:
		    user.not_seen = 0
		    user.seen = False
		    send = message(2, 'You have been logged out.')
		    try:
			clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clntSocket.connect((str(user.ip_address), user.port))
			clntSocket.send(send.message)
			clntSocket.close()
		    except socket.error, (value, label):
			print('Socket could not be opened: ' + label)
		    user.logged_in = False
		    user.ip_address = -1
		    user.port = -1
	    

