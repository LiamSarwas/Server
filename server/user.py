#########################
#Name: Liam Sarwas
#UNI: lms2260
#
#This class handles user
#information and status
########################


class User():  
    def __init__(self, username, password, ip_address, port, logged_in, times_failed, time_locked, seen, not_seen, messageList):
	self.username = username
	self.password = password
	self.ip_address = ip_address
	self.port = port
	self.logged_in = logged_in
	self.times_failed = times_failed
	self.time_locked = time_locked
	self.seen = seen
	self.not_seen = not_seen
	self.messageList = messageList
