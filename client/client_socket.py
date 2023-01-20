import socket
from config import *

class ClientSocket(socket.socket):
    
    def __init__(self):
        super(ClientSocket,self).__init__(socket.AF_INET, type=socket.SOCK_STREAM)
   
    def connect(self):
        super(ClientSocket,self).connect((SERVER_IP,SERVER_PORT))
        
    def recv_data(self):
        return self.recv(1024).decode('utf-8')
    
    def send_data(self,data):
        return self.send(data.encode('utf-8'))