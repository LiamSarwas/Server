#########################
#Name: Liam Sarwas
#UNI: lms2260
#
#This class aggregates user
#information and status
########################

from clntUser import User

class UserList():  
    def __init__(self, filepath):
	self.filepath = filepath
	self.userList = []
    
    def containsUser(self, key):
	contains = False
	for i in range(0, len(self.userList)):
	    if(self.userList[i].username == key):
		contains = True
	return contains

    def __len__(self):
	return len(self.userList)

    def __getitem__(self, key):
	return self.userList[key]

    def __setitem__(self, key, value):
	self.userList[key] = value
