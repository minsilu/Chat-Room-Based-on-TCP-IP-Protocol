from login import Login
from client_protocol import RespongeProtocol
from client_socket import ClientSocket
from threading import Thread
from config import *
from tkinter.messagebox import showinfo
from chat import Chat
import sys
from db import DataBase
from contact import Contact
from time import strftime, localtime, time
import os

class Client(object):
    def __init__(self):
        # 注册窗口
        self.window = Login()
        self.window.on_reset_click(self.clear_inputs)
        self.window.on_login_click(self.send_login_request)
        self.window.on_window_close(self.exit)
        
        # 聊天窗口
        self.window_chat = Chat()
        self.window_chat.withdraw() # 隐藏窗口
        self.window_chat.on_send_click(self.send_chat_request)
        self.window_chat.click_listbox_item(lambda event:self.enter_chat(event))
        self.window_chat.on_window_close(self.close_chat_window)
        
        # 联系人列表窗口
        self.window_contact = Contact()
        self.window_contact.withdraw()# 隐藏窗口
        self.window_contact.click_listbox_item(lambda event:self.change_chat(event))
        self.window_contact.on_window_close(self.exit)
        
        # 客户端套接字
        self.conn = ClientSocket()
        self.response_handle_funtion={}
        self.register(RESPONSE_LOGIN,self.response_login_handle)
        self.register(RESPONSE_CHAT,self.response_chat_handle)
        self.register(SYSTEM_MESSAGE,self.response_system_handle)
        
        # 当前登录用户
        self.username = None
        self.nickname = None
        self.toname = None # username or group
        self.chattype = None
        self.is_running = True
        self.friends = None
        self.groups = None
        
        # 数据库
        self.db = DataBase()

        # 消息缓冲区
        self.message_buffer = []

    
    def register(self,id,handle_function):
        self.response_handle_funtion[id]=handle_function
    

    
    def startup(self):
        self.conn.connect()
        Thread(target=self.response_handle).start()
        # 死循环，需要放在后边
        self.window.mainloop()


    def response_handle(self):
        while self.is_running:
            recv_data = self.conn.recv_data()
            
            parse_data = self.parse_response(recv_data)
            
            handle_function = self.response_handle_funtion.get(parse_data['id']) 
            if handle_function:
                handle_function(parse_data)

            
    def parse_response(self,recv_data):
        '''
        登录响应：1001|rat|nickname|username
        聊天响应：1002|nickname|message|fromwho|time
        系统消息：1003|message|fromwho
        '''
        response_data_list = recv_data.split(DELIMITER)
        response_data = {}
        response_data['id'] = response_data_list[0]
        if response_data['id'] == RESPONSE_LOGIN:
            response_data['rat'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
        if response_data['id'] == RESPONSE_CHAT:
            response_data['nickname'] = response_data_list[1]
            response_data['message'] = response_data_list[2]
            response_data['fromwho'] = response_data_list[3]
            response_data['time'] = response_data_list[4]
        if response_data['id'] == SYSTEM_MESSAGE:
            response_data['message'] = response_data_list[1]
            response_data['fromwho'] = response_data_list[2]
        return response_data
        
        
    def response_login_handle(self,parse_data):
        result = parse_data['rat']
        if result == '0':
            # 弹出一个对话框，提示登录失败
            showinfo('登录失败','用户名或密码错误')
            return
        
        self.nickname = parse_data['nickname']
        self.username = parse_data['username']
        self.friends = self.get_friends()
        self.groups = self.get_groups()
        self.window.withdraw() # 隐藏登录窗口
        
        # 获取历史数据
        self.load_history(self.groups)
        self.load_history(self.db.get_friends(self.username))
        
        self.window_contact.group_list = self.groups
        self.window_contact.friend_list = self.friends
        self.window_contact.refresh_listbox()
        self.window_contact.set_title(f'{self.nickname}的联系人列表')
        self.window_contact.update()
        self.window_contact.deiconify() # 设置联系人列表窗口标题    
        
    
    def response_chat_handle(self,parse_data):
        self.message_buffer.append(parse_data)
        self.record_message(parse_data)
        # print(parse_data)
        if parse_data['fromwho'] == self.toname:
            self.window_chat.append_msg(parse_data['nickname'], parse_data['message'], parse_data['time'])
        
    
    def response_system_handle(self,parse_data):
        # self.message_buffer.append(parse_data)
        if parse_data['fromwho'] == self.toname:
            self.window_chat.append_system_msg(parse_data['message'])

    def load_history(self, list):
        if list is None:
            return
        for item in list:
            self.read_my_message(item)
    

    def send_login_request(self):
        username = self.window.get_username()
        password = self.window.get_password()
        request_text = RespongeProtocol.request_login(username, password)
        self.conn.send_data(request_text)
        

    def send_chat_request(self):
        msg = self.window_chat.get_input()
        self.window_chat.clear_input()
        self.store_my_message(msg)
        
        if self.chattype == 'friend':
            request_text = RespongeProtocol.request_onechat(self.username, msg, self.toname)
        if self.chattype == 'group':
            request_text = RespongeProtocol.request_groupchat(self.username, msg, self.toname)
        self.conn.send_data(request_text)    
    
    
    def record_message(self, parse_data):
        path = f'record/{self.username}'
        if not os.path.exists(path):
            os.makedirs(path)
        
        name = parse_data['fromwho']
        f = open(path + f'/{name}.txt', 'a')
        
        # f = open(path + f'/{self.toname}.txt', 'a')
        f.write(parse_data['nickname'] + ',' + parse_data['message'] + ',' + parse_data['time'])
        f.write('|')

        f.close()

    def read_my_message(self,fromwho):
        path = f'record/{self.username}/{fromwho}.txt'
        if not os.path.exists(path):
            print('no record')
            return 
        f = open(path, 'r')
        text = f.read()
        f.close()
        
        text = text.split('|')
        # print(text)
        
        for i in range(0,len(text)-1):
            data={}
            temp = text[i]
            temp = temp.split(',')
            # print(i,temp)
            data['nickname'] = temp[0]
            data['message'] = temp[1]
            data['time'] = temp[2]
            data['fromwho'] = fromwho
            self.message_buffer.append(data)
        
        # print(self.message_buffer)
    
    
    def clear_inputs(self):
        self.window.clear_username()
        self.window.clear_password()    
    
    
    def change_chat(self, event):
        toname, chattype = self.window_contact.get_listbox_select(event)
        if toname == None:
            return
        
        if self.chattype == 'group':
            self.send_groupexit_request()
        
        self.chattype = chattype    
        self.window_chat.clear_chat_area()
        
        if self.chattype == 'friend':
            self.toname = toname['username']
            toname = toname['nickname']
            self.window_chat.set_title(f'与{toname}的聊天')
            self.window_chat.user_list = []
        if self.chattype == 'group':
            self.toname = toname
            self.window_chat.set_title(f'群聊{toname}的聊天室')
            self.window_chat.user_list = self.get_group_members(toname)
            self.window_chat.append_system_msg(f'欢迎来到{toname}的聊天室')
            self.send_groupenter_request()
        
        # self.read_my_message(self.toname)
        for message in self.message_buffer:
            if message['fromwho'] == self.toname:
                if message['nickname'] == self.nickname:
                    self.window_chat.append_my_msg(self.nickname,message['message'], message['time'])
                else:
                    self.window_chat.append_msg(message['nickname'], message['message'], message['time'])  
        
        self.window_chat.refresh_user_listbox()
        self.window_chat.update()
        self.window_chat.deiconify() 
        
        
    
    def enter_chat(self,event):
        toname = self.window_chat.get_listbox_select(event)
        if self.chattype == 'group':
            self.send_groupexit_request()
        
        self.toname = toname['username']
        toname = toname['nickname']
        self.window_chat.set_title(f'与{toname}的聊天')
        self.chattype = 'friend'
        
        self.window_chat.user_list = []
        
        self.window_chat.clear_chat_area()
        # self.read_my_message(self.toname)
        for message in self.message_buffer:
            if message['fromwho'] == self.toname:
                if message['nickname'] == self.nickname:
                    self.window_chat.append_my_msg(self.nickname,message['message'], message['time'])
                else:
                    self.window_chat.append_msg(message['nickname'], message['message'], message['time'])  
        self.window_chat.refresh_user_listbox()
        self.window_chat.update()
        self.window_chat.deiconify()   
    


        
    def store_my_message(self,msg):
        my_data = {}
        my_data['nickname'] = self.nickname
        my_data['message'] = msg
        my_data['time'] = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        my_data['fromwho'] = self.toname
        self.message_buffer.append(my_data)
        self.window_chat.append_my_msg(self.nickname, msg, my_data['time'])
        self.record_message(my_data)
        
    
    
    
    def send_groupenter_request(self):
        msg =f'{self.nickname}进入聊天室'
        request_text = RespongeProtocol.request_groupenter(self.username, msg, self.toname)
        self.conn.send_data(request_text)
        # print(request_text)
    
    def send_groupexit_request(self):
        msg =f'{self.nickname}退出聊天室'
        request_text = RespongeProtocol.request_groupexit(self.username, msg, self.toname)
        self.conn.send_data(request_text)
        # print(request_text)
    
    def exit(self):
        if self.chattype == 'group':
            self.send_groupexit_request()
        self.is_running = False
        self.conn.close()
        sys.exit(0)
    
    def close_chat_window(self):
        if self.chattype == 'group':
            self.send_groupexit_request()
        self.window_chat.withdraw()
    
    def get_friends(self):
        friends = self.db.get_friends(self.username)
        friends_list = []
        if friends == None:
            return friends_list
        for friend in friends:
            one_friend = self.db.get_one(friend)
            friends_list.append({'username':one_friend['user_name'],'nickname':one_friend['user_nickname']})
        return friends_list
    
    def get_group_members(self, groupname):
        members = self.db.get_group_members(groupname)
        members_list = []
        if members == None:
            return members_list
        for member in members:
            one_member = self.db.get_one(member)
            members_list.append({'username':one_member['user_name'],'nickname':one_member['user_nickname']})
        return members_list
    
    
    def get_groups(self):
        groups = self.db.get_groups(self.username)
        if groups == None:
            return []
        return groups
    
    
    
if __name__ == '__main__':
    client=Client()
    # client.message_buffer.append({'fromwho':'study','nickname':'test','message':'test','time':'test1'})
    # client.message_buffer.append({'fromwho':'study','nickname':'test','message':'test','time':'test2'})
    client.startup()
    
    # client.read_my_message()
    # client.window.mainloop()

 
