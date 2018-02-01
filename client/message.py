#########################
#Name: Liam Sarwas
#UNI: lms2260
#
#This class aggregates user
#information and status
########################

class message():  
    def __init__(self, value, string):
	self.value = value
	self.string = string
	self.length = len(self.string)
	self.message = '{},{},{}'.format(self.value, self.length, self.string)

    def __len__(self):
	return len(message)
