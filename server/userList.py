#########################
#Name: Liam Sarwas
#UNI: lms2260
#
#This class aggregates user
#information and status
########################

from user import User

class UserList():  
    def __init__(self, filepath):
	self.filepath = filepath
	self.userList = []
	self.blockedMatrix = []
	self.makeList()
	self.blockSetup()

    def makeList(self):
	credentials = open(self.filepath)
	for line in credentials:
	    linelist = line.split(' ')
	    self.userList.append(User(linelist[0].strip(), linelist[1].strip(), -1, -1, False, 0, -1, False, 0, []))
    
    def blockSetup(self):
    	self.blockedMatrix = [[0]*(len(self.userList)) for i in range(0, len(self.userList))]

    def isBlocked(self, blocker, blocked):
	blockerNum = 0
	blockedNum = 0
	for i in range(0, len(self.userList)):
	    if(blocker == self.userList[i].username):
		blockerNum = i
	    if(blocked == self.userList[i].username):
		blockedNum = i
	if(self.blockedMatrix[blockerNum][blockedNum] != 1):
	    return False
	else:
	    return True

    def setBlocked(self, blocker, blocked):
	blockerNum = 0
	blockedNum = 0
	for i in range(0, len(self.userList)):
	    if(blocker == self.userList[i].username):
		blockerNum = i
	    if(blocked == self.userList[i].username):
		blockedNum = i
	self.blockedMatrix[blockerNum][blockedNum] = 1

    def setUnblocked(self, blocker, blocked):
	blockerNum = 0
	blockedNum = 0
	for i in range(0, len(self.userList)):
	    if(blocker == self.userList[i].username):
		blockerNum = i
	    if(blocked == self.userList[i].username):
		blockedNum = i
	self.blockedMatrix[blockerNum][blockedNum] = 0
    
    def getUserIndexByName(self, username):
	user_num = None
	for i in range(0, len(self.userList)):
	    if(username == self.userList[i].username):
		user_num = i
	return user_num

    def getUserIndexByIP(self, ip_address):
	user_num = None
	for i in range(0, len(self.userList)):
	    if(ip_address == self.userList[i].ip_address):
		user_num = i
	return user_num

    def __len__(self):
	return len(self.userList)

    def __getitem__(self, key):
	return self.userList[key]

    def __setitem__(self, key, value):
	self.userList[key] = value
