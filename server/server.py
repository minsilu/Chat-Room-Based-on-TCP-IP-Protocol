from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from threading import Thread
from protocol import *
from db import DataBase

class Server(object):
        def __init__(self):
            # 服务器套接字
            self.server = ServerSocket()
            self.clients = {}
            
            # ID对应的处理方法
            self.request_handle_funtion={}
            self.register(REQUEST_LOGIN,self.request_login_handle)
            self.register(REQUEST_CHAT,self.request_chat_handle)
            
            # 当前登录用户
            self.current_user = {}
            
            # 数据库
            self.db = DataBase()

            # 当前发送的目标用户
            # self.toname = []

        # 注册消息类型和处理方法
        def register(self,id,handle_function):
            self.request_handle_funtion[id]=handle_function
    
         
        def startup(self):
            print(f'Server is running at {SERVER_IP}:{SERVER_PORT}') 
            while True:
                client, addr = self.server.accept()
                client_socket = SocketWrapper(client) 
                Thread(target=lambda:self.request_handle(client_socket)).start()

                
        def request_handle(self, client_socket):
            while True:
                msg = client_socket.recv_data()
                if not msg:
                    self.remove_offline(client_socket)
                    client_socket.close()
                    break
                # print(msg)
                # client_socket.send_data('服务器收到的是:'+ msg)
                
                # 解析数据
                parse_data = self.parse_request(msg)
                # print(parse_data)
                
                handle_function = self.request_handle_funtion.get(parse_data['id']) 
                if handle_function:
                    handle_function(client_socket, parse_data)
                
                      
        def remove_offline(self,client_socket):
            # print('进入函数 remove_offline')
            for username, info in self.current_user.items():
                if info['sock'] == client_socket:
                    # print(self.current_user)
                    del self.current_user[username]
                    # print(self.current_user)
                    break
           
                
        def parse_request(self, msg):
            '''
            登录信息：0001|username|password
            聊天信息：0002|username|message|towho|to_type|time
            '''
            request_list = msg.split(DELIMITER)
            request_data = {}
            request_data['id']=request_list[0]
            if request_data['id'] == REQUEST_LOGIN:
                request_data['username']=request_list[1]
                request_data['password']=request_list[2]
            elif request_data['id'] == REQUEST_CHAT:
                request_data['username']=request_list[1]
                request_data['message']=request_list[2]
                request_data['towho']=request_list[3]
                request_data['to_type']=request_list[4]
                request_data['time']=request_list[5]
            return request_data


        def request_login_handle(self, client_socket, request_data):
            username = request_data['username']
            password = request_data['password']
            ret, nickname, username = self.check_user_login(username, password)
            if ret == '1':
                self.current_user[username] = {'sock':client_socket, 'nickname':nickname}
            
            response_text = RespongeProtocol.response_login(ret, nickname, username)
            client_socket.send_data(response_text)
            # print('进入函数 request_login_handle')
            
        
        def request_chat_handle(self, client_socket, request_data):
            # 聊天信息：0002|username|message|towho|to_type|time
            # 聊天响应：1002|nickname|message|fromwho|time
            # 系统消息：1003|message|fromwho
            
            username = request_data['username']
            message = request_data['message']
            time = request_data['time']
            nickname = self.current_user[username]['nickname'] 
            send_list = []
            
            if request_data['to_type'] == '1':
                send_list.append(request_data['towho'])
                msg = RespongeProtocol.response_chat(nickname, message, username, time)
            
            if request_data['to_type'] == '2':
                send_list = self.db.get_group_members(request_data['towho'])
                msg = RespongeProtocol.response_chat(nickname, message, request_data['towho'], time)
            
            if request_data['to_type'] == '3' or request_data['to_type'] == '4':
                send_list = self.db.get_group_members(request_data['towho'])
                msg = RespongeProtocol.response_system(message, request_data['towho'])
            
            for u_name, info in self.current_user.items():
                if u_name == username:
                    continue
                if u_name in send_list:
                    info['sock'].send_data(msg)
          
            
        def check_user_login(self, username, password):
            query_result = self.db.get_one(username)
            # print(query_result)
            if not query_result:
                return '0', '', username
            if query_result['user_password'] != password:
                return '0', '', username
            return '1', query_result['user_nickname'], query_result['user_name']

        
        # def get_group_members(self, groupname):
        #     members = self.db.get_group_members(groupname)
        #     members_list = []
        #     if members == None:
        #         return members_list
        #     for member in members:
        #         one_member = self.db.get_one(member)
        #         members_list.append({'username':one_member['user_name'],'nickname':one_member['user_nickname']})
        #     return members_list        
        
if __name__ == '__main__':
    Server().startup()
 

