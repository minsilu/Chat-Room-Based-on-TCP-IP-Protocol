
class SocketWrapper(object):
        def __init__(self,socket):
            self.socket = socket
        
        def recv_data(self):
            return self.socket.recv(1024).decode('utf-8')
        
        def send_data(self,data):
            return self.socket.send(data.encode('utf-8'))
        
        def close(self):
            self.socket.close()