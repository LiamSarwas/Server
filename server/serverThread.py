import threading
import sys
import socket
import collections
import time
import config
from message import message

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
    
    #is the message a login message
    if(messages[0] == 0):
	userpassport = messages[2].split(' ')
	user_num = config.users.getUserIndexByName(userpassport[0])
	if(user_num == None):
	    #send an error message telling the client that the user isnt in the system
	    output = message(-1, "That username is not in the system.")	
	    conn.send(output.message)
	    return -1
	
	#handles the log in process
	if(time.time() - config.users[user_num].time_locked > 60):
	    config.users[user_num].time_locked = -1
	    if(config.users[user_num].times_failed < 3):
		if(config.users[user_num].password == userpassport[1]):
		    if(config.users[user_num].logged_in == False or address[0] == config.users[user_num].ip_address):
			#logged in normally
			config.users[user_num].logged_in = True
			config.users[user_num].times_failed = 0
			config.users[user_num].ip_address = address[0]
			config.users[user_num].port = int(userpassport[2])
			output = message(2, "Welcome to the simple chat room.")
			conn.send(output.message)
			sendUsers(user_num)
			sendOfflineMessages(user_num)
			return 1
		    else:
			#logged in from a second ip address
			send = message(2, 'You have logged in elsewhere. Goodbye.')
			try:
			    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			    clntSocket.connect((str(config.users[user_num].ip_address), config.users[user_num].port))
			    clntSocket.send(send.message)
			    clntSocket.close()
			except socket.error, (value, label):
			    print('Socket could not be opened: ' + label)
			config.users[user_num].logged_in = True
			config.users[user_num].times_failed = 0
			config.users[user_num].ip_address = address[0]
			config.users[user_num].port = int(userpassport[2])
			output = message(2, "Welcome to the simple chat room.")
			conn.send(output.message)
			sendUsers(user_num)
			sendOfflineMessages(user_num)
			return 1
		else:
		    if(config.users[user_num].times_failed == 2):
			config.users[user_num].times_failed = 0
			config.users[user_num].time_locked = time.time()		
			output = message(-1, 'Due to repeated login failures you have been locked out of this account. Please try again later.')
			conn.send(output.message)	
			return -1
		    else:
			config.users[user_num].times_failed += 1
			output = message(-1, 'Wrong password, please try again.')
			conn.send(output.message)
			return -1
	else:
	    output = message(-1, 'Your account is still locked out. Please try again later.')
	    conn.send(output.message)
	    return -1
    
    #is the message a message to another client
    if(messages[0] == 1):
	usermess = messages[2].split(' ')
	receiver = usermess[0]
	mess = ''
	for i in range(1, len(usermess)):
            mess = mess + usermess[i] + ' '

	user_num = config.users.getUserIndexByName(receiver)	
	sender = ''
	for user in config.users:
	    if(address[0] == user.ip_address):
		sender = user.username

	if(config.users[user_num].logged_in == 1): 
	    if(not config.users.isBlocked(receiver, sender)):
		#send a receipt to the sending client
		send = message(1, 'Message sent')
		conn.send(send.message)

		#send the message to the receiving client
		output = message(1, sender + ' ' + mess)
		try:
		    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    clntSocket.connect((str(config.users[user_num].ip_address), config.users[user_num].port))
		    clntSocket.send(output.message)
		    clntSocket.close()
		except socket.error, (value, label):
		    print('Socket could not be opened: ' + label)
		    config.users[user_num].logged_in = False
		    config.users[user_num].ip_address = -1
		    config.users[user_num].port = -1

		return 1
	    else:
		#send error message back saying that they are blocked
		output = message(-1, 'You have been blocked by user {} and your message was not sent'.format(receiver))
		conn.send(output.message)
		return 1
	else:
	    #send error message saying that they arent logged in
	    output = message(-1, 'That user is not logged in right now.\n They will receive your message when they log in.')
	    conn.send(output.message)
	    saved = message(sender, messages[2])
	    config.users[user_num].messageList.append(saved)
	    return 1

    #if this is a block request
    if(messages[0] == 2):
	blocked = messages[2]
	user_num = config.users.getUserIndexByName(blocked)
	for user in config.users:
	    if(address[0] == user.ip_address):
		blocker = user.username
	config.users.setBlocked(blocker, blocked)
	output = message(2, 'User {} was blocked.'.format(blocked))
	conn.send(output.message)
	return 1
    
    #if this is a unblock request
    if(messages[0] == 3):
	blocked = messages[2]
	user_num = config.users.getUserIndexByName(blocked)
	for user in config.users:
	    if(address[0] == user.ip_address):
		blocker = user.username
	config.users.setUnblocked(blocker, blocked)
	output = message(2, 'User {} was unblocked.'.format(blocked))
	conn.send(output.message)
	return 1

    #if this is an online request
    if(messages[0] == 4):
	onlineUsers = ''
	for user in config.users:
	    if(user.logged_in == True):
		onlineUsers = onlineUsers + user.username + ' '
	output = message(2, 'The following users are online: {}'.format(onlineUsers))
	conn.send(output.message)
	return 1

    #if this is a broadcast request
    if(messages[0] == 5):
	mess = messages[2]
	blocked = False
	sender = ''
	for user in config.users:
	    if(address[0] == user.ip_address):
		sender = user.username
		
	for user in config.users:
	    if(user.logged_in == True):
		if(not config.users.isBlocked(user.username, sender)):
		    #send the message to the receiving client
		    output = message(1, sender + ' ' + mess)
		    try:
			clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    	clntSocket.connect((str(user.ip_address), user.port))
		    	clntSocket.send(output.message)
		    	clntSocket.close()
		    except socket.error, (value, label):
			print 'Socket could not be opened: ' + label
		else:
		    #set it so that we know that at least one user has the sender blocked
		    blocked = True
	    else:
		if(not config.users.isBlocked(user.username, sender)):
		    #save the message to be seen later
		    saved = message(sender, messages[2])
		    user.messageList.append(saved)

 	#send a receipt to the sending client
	if(blocked == False):
	    send = message(1, 'Messages sent')
	    conn.send(send.message)
	    return 1
	else:
	    send = message(2, 'Your message could not be delivered to all recipients.')
	    conn.send(send.message)
	    return 1
    
    #if this is a getaddress request
    if(messages[0] == 6):
	username = messages[2]
	sender_num = config.users.getUserIndexByIP(address[0])
	sender = config.users[sender_num].username
	if(not config.users.isBlocked(username, sender)):
	    ip = ''
	    port = -1
	    for user in config.users:
		if(username == user.username):
		    port = user.port
		    ip = user.ip_address
	    send = message(3, username + ' ' + str(ip) + ' ' + str(port))
	    conn.send(send.message)
	else:
	    send = message(2, 'You have been blocked by this user and cannot request their private information')
	    conn.send(send.message)
	return 1
    
    #if this is a logout request
    if(messages[0] == 7):
	user_num = config.users.getUserIndexByIP(address[0])
	config.users[user_num].logged_in = False
	config.users[user_num].ip_address = -1
	config.users[user_num].port = -1
	send = message(2, 'You are now logged out.')
	conn.send(send.message)
	return 1

    #if this is a heartbeat
    if(messages[0] == 8):
	user = messages[2]
	user_num = config.users.getUserIndexByName(user)	
	config.users[user_num].seen = True
	return 1

def sendUsers(user_num):
    '''
    Sends the list of users to the client
    '''
    userlist = ''
    for user in config.users:
	userlist = userlist + user.username + ' '
    userlist = userlist.strip()
    output = message(4, userlist)
    try:
	clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clntSocket.connect((str(config.users[user_num].ip_address), config.users[user_num].port))
	clntSocket.send(output.message)
	clntSocket.close()
    except socket.error, (value, label):
	print('Socket could not be opened: ' + label)



def sendOfflineMessages(user_num):
    '''
    Sends the user all of the messages they received while offline
    '''
    length = len(config.users[user_num].messageList)
    output = message(3, 'You have {} unread messages.\n'.format(length))
    try:
	clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clntSocket.connect((str(config.users[user_num].ip_address), config.users[user_num].port))
	clntSocket.send(output.message)
	clntSocket.close()
    except socket.error, (value, label):
	print('Socket could not be opened: ' + label)

    for mess in config.users[user_num].messageList:
	output = mess
	try:
	    clntSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    clntSocket.connect((str(config.users[user_num].ip_address), config.users[user_num].port))
	    clntSocket.send(output.message)
	    clntSocket.close()
	except socket.error, (value, label):
	    print('Socket could not be opened: ' + label)

class ServerThread (threading.Thread):
    def __init__(self, conn, address):
	threading.Thread.__init__(self)
	self.conn = conn
	self.address = address

    def run(self):
	serverThreadMain(self.conn, self.address)


def serverThreadMain(conn, address):
    while 1:
	output = receive(conn, address)
	if(output == 1):
	    break
    conn.close()
