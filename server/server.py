################################
#Author - Liam Sarwas, lms2260 #
#                              #
#This is the server end of the # 
#chat room.                    #
################################
import sys
import socket
import collections
import time
import config
from message import message
from serverThread import ServerThread
from serverHeartbeatThread import ServerHeartbeatThread

def startUp():
    if(len(sys.argv) != 2):
    	print 'Usage: python {} <server_port>'.format(sys.argv[0])
    	quit()
    config.port = ''
    config.port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.host, config.port))
    heartbeatListener = ServerHeartbeatThread(30)
    heartbeatListener.daemon = True
    heartbeatListener.start()
    return s

def main():
    serverSocket = startUp()
    while 1:
	serverSocket.listen(1)
	conn, address = serverSocket.accept()
	print 'Connected by', address
	serverThread = ServerThread(conn, address)
	serverThread.daemon = True
	serverThread.start()

try:
    main()
except KeyboardInterrupt:
    print 'Shutting down the server.'
    sys.exit(0)
    raise
