from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Listbox



class Contact(Toplevel):
    def __init__(self):
        super(Contact,self).__init__()
        # self.title('home')
        self.user = {"nickname":"amber","username":"user1"}
        self.friend_list = [{'nickname':'candy','username':'user3'}, {'nickname':'bob','username':'user2'}]
        self.group_list =['group1','group2']
        
        window_width = 260
        window_height = 600
        screen_width = self.winfo_screenwidth()
        # 显示在屏幕右上角
        pos_x = (screen_width - window_width) -30
        pos_y = 10
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))
        self.resizable(0, 0)
        self.title('联系人列表')
        
        self.add_widgets()
        self.click_listbox_item(lambda event: self.get_listbox_select(event))

    
    def add_widgets(self):
        # scroll = Scrollbar(self)
        # scroll.pack(fill='both', expand=True)
        # 增加一项，用于显示好友列表
        

        listbox = Listbox(self,width=50, height=50,bg='#EEE',name='listbox')
        listbox.grid(row=0, column=0)
        self.refresh_listbox()
        
        # button_frame = Frame(self,name='button_frame')
        # add_friend = Button(button_frame, text="添加好友",name='add_friend')
        # add_friend.pack(side='left', expand=True, fill='x')

        # add_room = Button(button_frame, text="添加聊天室",name='add_room')
        # add_room.pack(side='left', expand=True, fill='x')

        # create_room = Button(button_frame, text="创建聊天室",name='create_room')
        # create_room.pack(side='left', expand=True, fill='x')

        # button_frame.pack(expand=False, fill='x')
        
        
    def refresh_listbox(self):
        self.children['listbox'].delete(0, 'end')
        
        for group in self.group_list:
            self.children['listbox'].insert(0, group)
            self.children['listbox'].itemconfig(0, fg='blue')
        self.children['listbox'].insert(0, '群聊列表')
        
        for friend in self.friend_list:
            self.children['listbox'].insert(0, '昵称：'+ friend['nickname']+'  账号:'+friend['username'])
            self.children['listbox'].itemconfig(0, fg='green')
        self.children['listbox'].insert(0, '好友列表')
        
        
    # def on_add_friend_click(self, command):
    #     self.children['button_frame'].children['add_friend']['command']=command
    
    # def on_add_room_click(self, command):
    #     self.children['button_frame'].children['add_room']['command']=command
        
    # def on_create_room_click(self, command):
    #     self.children['button_frame'].children['create_room']['command']=command
    
    def set_title(self, title):
        self.title(title)
    
    def click_listbox_item(self, command):
        self.children['listbox'].bind('<Double-Button-1>', command)
    
    def get_listbox_select(self, event):
        # 获取当前选中的item
        cur_item = self.children['listbox'].curselection()
        index = cur_item[0]
        # 获取当前选中的用户名
        if index == 0 or index == len(self.friend_list) + 1:
            return
        elif index <= len(self.friend_list):
            item = self.friend_list[len(self.friend_list) - index]
            type = 'friend'
        else:
            item = self.group_list[len(self.friend_list) + len(self.group_list) + 1 - index]
            type = 'group'
        # print(item, type)
        return item, type
    
    def on_window_close(self, command):
        self.protocol('WM_DELETE_WINDOW', command)
    
    
    
    
if __name__ == '__main__':
    chat = Contact()
    chat.mainloop()