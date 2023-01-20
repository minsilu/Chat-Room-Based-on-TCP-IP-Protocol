import socket
from config import *


# 服务器初始化
class ServerSocket(socket.socket):

    def __init__(self):
        super(ServerSocket,self).__init__(socket.AF_INET, type=socket.SOCK_STREAM)
        self.bind((SERVER_IP, SERVER_PORT))
        self.listen(256)