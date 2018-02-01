CODE STRUCTURE and DATA STRUCTURES

The general structure of my program is in two large sections, each with their
own subjections. The server side starts with server.py which starts up the
server and listens for user connections. It handles each user on a seperate
thread from the serverThread.py module. It checks for the heartbeat updates
from the user with a seperate thread from the serverHeartbeatThread.py module.
All of the user information is stored in a UserList (from the userList.py
module) that is held in the config.py file where all of the threads can easily
access and modify it.

The client side starts with the client.py file which handles all of the user
input and starts the necessary threads. The loginThread.py handles the initial
login of the client, and has to terminate before the user can do anything
else. The receiverThread handles all incoming connections (i.e. when the
server requests a connection to pass it a message or if another user wants to
send a private message). The clientThread handles all of the communication to
the server. The client also maintains a list of user information as a
clntUserList and is stored in the client copy of config.py.

Both the server and client have a user.py class which is what the UserList is
comprised of. It is simply a collection of data about the user (ip_address,
port, whether they are logged in or not). The server also maintains a matrix
representing the blocking status of all of the users. 

RUNNING MY CODE
In order to run my code, simply leave all of the files as they are (all of the
client files in the client folder, all of the server files in the server
folder). If there are changes to the credentials.txt file, make sure to put
that back in the server folder.  From within the server folder, run the following command to start the server (where <port_number> is the port that the server will be listening):

python server.py <port_number>

To start a client session run the following command from inside the client
folder:

python client.py <hostname> <host_port_number> <client_port_number>

The hostname is the hostname of the location that server.py is being run from,
the host port number is the port that the server is listening to, and the
client port number is the port that the client will be listening to to receive
messages from the server and other clients directly.

Once started, simply type help to get started and learn about the commands
that the client and server have implemented.

EXAMPLE (on delhi.clic.cs.columbia.edu for example):
(from within /server/)
python server.py 8080

(from within /client/)
python client.py delhi.clic.cs.columbia.edu 8080 8888
