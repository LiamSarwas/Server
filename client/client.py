###################
#Author: Liam Sarwas, lms2260
#
#This is the main client program.
#It handles the creation of the various threads that will handle all necessary connections
###################
import socket
import sys
import threading
import time
import config

from clientThread import clientThread
from loginThread import loginThread
from receiveThread import receiveThread
from heartbeatThread import heartbeatThread
from message import message

def parseInput(userInput):
    '''
    Parses user input and decides what to do with it
    '''
    inputList = userInput.split(' ')
    length = len(inputList)
    
    #if the user wants to send a message
    if(inputList[0] ==  'message'):
	if(length >= 3):
	    if(config.users.containsUser(inputList[1])):
		mess = ''
		for i in range(2, len(inputList)):
		    mess = mess + inputList[i] + ' ' 
		send = message(1, inputList[1] + ' ' + mess)
		return send
	    else:
		print('That user is not in the system.')
	else:
	    print('Command usage: message <username> <message>')

    #if the user wants to block another user
    elif(inputList[0] == 'block'):
	if(length == 2):
	    if(config.users.containsUser(inputList[1])):
		send = message(2, inputList[1])
		return send
	    else:
		print('That user is not in the system.')
	else:
	    print('Command usage: block <username>')
    
    #if the user wants to unblock another user
    elif(inputList[0] == 'unblock'):
	if(length == 2):
	    if(config.users.containsUser(inputList[1])):
		send = message(3, inputList[1])
		return send
	    else:
		print('That user is not in the system.')
	else:
	    print('Command usage: unblock <username>')
    
    #if the user wants to see who else is online
    elif(inputList[0] == 'online'):
	if(length == 1):
	    send = message(4, '')
	    return send
	else:
	    print('Command usage: online')
    
    #if the user wants to send a message to all users 
    elif(inputList[0] ==  'broadcast'):
	if(length >= 2):
	    mess = ''
	    for i in range(1, len(inputList)):
		mess = mess + inputList[i] + ' ' 
	    send = message(5, mess)
	    return send
	else:
	    print('Command usage: broadcast <message>')
    
    #if the user wants another users ip_address and port
    elif(inputList[0] == 'getaddress'):
	if(length == 2):
	    if(config.users.containsUser(inputList[1])):
		send = message(6, inputList[1])
		return send
	    else:
		print('That user is not in the system.')
	else:
	    print('Command usage: getaddress <username>')

    #if the user wants to send a message directly to another user
    elif(inputList[0] == 'private'):
	if(length >= 3):
	    if(config.users.containsUser(inputList[1])):
		user_num = 0
		for i in range(0, len(config.users)):
		    if(inputList[1] == config.users[i].username):
			user_num = i
		if(config.users[user_num].ip_address == -1 or config.users[user_num].port == -1):
		    send = message(6, inputList[1])
		    messageSender = clientThread(config.serverHostname, config.serverPort, send)
		    messageSender.daemon = True
		    messageSender.start()
		    messageSender.join()
		    if(str(config.users[user_num].ip_address) != '-1' and int(config.users[user_num].port) != -1):
			mess = ''
			for i in range(2, len(inputList)):
			    mess = mess + inputList[i] + ' ' 
			send = message(1, config.currentUser + ' ' + mess)
			try:
			    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			    clntSocket.connect((str(config.users[user_num].ip_address), int(config.users[user_num].port)))
			    clntSocket.send(send.message)
			    clntSocket.close()
			except socket.error, (value, label):
			    print('Socket could not be opened: ' + label)
		    return None
		else:
		    mess = ''
		    for i in range(2, len(inputList)):
			mess = mess + inputList[i] + ' ' 
		    send = message(1, config.currentUser + ' ' + mess)
		    try:
			clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clntSocket.connect((str(config.users[user_num].ip_address), int(config.users[user_num].port)))
			clntSocket.send(send.message)
			clntSocket.close()
		    except socket.error, (value, label):
			print('Socket could not be opened: ' + label)
		    return None
	    else:
		print('That user is not in the system.')
	else:
	    print('Command usage: private <username> <message>')

    #if the user wants to log out
    elif(inputList[0] == 'logout'):
	if(length == 1):
	    send = message(7, '')
	    messageSender = clientThread(config.serverHostname, config.serverPort, send)
	    messageSender.daemon = True
	    messageSender.start()
	    messageSender.join()
	    sys.exit(0)
	    return None
	else:
	    print('Command usage: logout')

    #if the user needs help using the commands
    elif(inputList[0] == 'help'):
	if(length == 1):
	    print('The following commands are recognized by the chat room: ')
	    print('message, private, broadcast, block, unblock, getaddress, logout')
	    print('To see how to use a command type help <command>')
	elif(length == 2):
	    if(inputList[1] == 'message'):
		print('Command usage: message <username> <message>')
	    elif(inputList[1] == 'private'):
		print('Command usage: private <username> <message>')
	    elif(inputList[1] == 'broadcast'):
		print('Command usage: broadcast <message>')
	    elif(inputList[1] == 'block'):
		print('Command usage: block <username>')
	    elif(inputList[1] == 'unblock'):
		print('Command usage: unblock <username>')
	    elif(inputList[1] == 'getaddress'):
		print('Command usage: getaddress <username>')
	    elif(inputList[1] == 'logout'):
		print('Command usage: logout')
	    else:
		print('That is not a recognized command. Type help to see a list of commands.')
	else:
	    print('Command usage: help or help <command>')
    else:
	print('That is not a recognized command. Type help to see a list of commands.')

def main():
    '''
    Starts the client and all of the necessary threads.
    '''

    if(len(sys.argv) != 4):
	print 'Usage: python {} <host_name> <host_port> <client_port>'.format(sys.argv[0])
	quit()
    
    config.serverHostname = sys.argv[1]
    config.serverPort = int(sys.argv[2])
    config.clientPort = int(sys.argv[3])


    #the receive thread handles all the connection requests (from the server or p2p)
    receive = receiveThread(config.clientPort)
    receive.daemon = True
    receive.start()

    #the login thread handles the initial login process
    login = loginThread(config.serverHostname, config.serverPort, config.clientPort)
    login.start()
    login.join()

   # once authenticated, start the heartbeat
    heartbeat = heartbeatThread(30,  config.serverHostname, config.serverPort)
    heartbeat.daemon = True
    heartbeat.start()

    while(True):

	userInput = raw_input()
	send = parseInput(userInput)

	if(send != None):
	    #handles sending all client/server messages
	    #p2p messages are dealt with in parseInput()
	    messageSender = clientThread(config.serverHostname, config.serverPort, send)
	    messageSender.daemon = True
	    messageSender.start()
	    messageSender.join()

    while True:
	time.sleep(1)


try:
    main()
except KeyboardInterrupt:
    send = message(7, '')
    messageSender = clientThread(config.serverHostname, config.serverPort, send)
    messageSender.daemon = True
    messageSender.start()
    messageSender.join()
    print 'Shutting down the chat room.'
    sys.exit(0)
    
    raise
