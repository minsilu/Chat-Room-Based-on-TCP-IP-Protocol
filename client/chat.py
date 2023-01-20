from tkinter import Toplevel
from tkinter import Label
from tkinter import Text
from tkinter import Button
from tkinter.scrolledtext import ScrolledText
from tkinter import Frame
from time import strftime, localtime, time
from tkinter import Listbox

class Chat(Toplevel):
    def __init__(self):
        super(Chat,self).__init__()
        # self.title('home')
        
        window_width = 890
        window_height = 505
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))
        self.resizable(0, 0)
        
        self.user_list = [{'nickname':'amber','username':'user1'}, {'nickname':'bob','username':'user2'}]
        
        self.add_widgets()
        self.set_title('home')
        self.on_send_click(lambda : self.append_msg('me', '666666'))
        self.refresh_user_listbox()
        # 显示对应item的用户名
        self.click_listbox_item(lambda event: self.get_listbox_select(event))

    
    def add_widgets(self):
        # 聊天区
        chat_area = ScrolledText(self, width=110, height=30)
        chat_area.grid(row=0, column=0,columnspan=2)
        chat_area.tag_config('green', foreground='#008B00')
        chat_area.tag_config('blue', foreground='#0000FF')
        chat_area.tag_config('system', foreground='gray')
        self.children['chat_area']=chat_area
        
        # 输入区
        input_area = Text(self,name='input_area', width=100, height=7)
        input_area.grid(row=1, column=0,pady=10)
        
        
        # 发送按钮
        sent_button = Button(self, name='sent_button',text='发送', width=5, height=2)
        sent_button.grid(row=1, column=1)
        
        # 成员区
        member_listbox = Listbox(self,width=15, height=30,bg='#EEE',name='member_listbox')
        member_listbox.grid(row=0, column=2,rowspan=2)
        

    
    def refresh_user_listbox(self):
        # user_list = ['user1', 'user2', 'user3']
        self.children['member_listbox'].delete(0, 'end')
        for user in self.user_list:
            self.children['member_listbox'].insert(0, user['nickname'])
            self.children['member_listbox'].itemconfig(0, fg='blue')
    
    def click_listbox_item(self, command):
        self.children['member_listbox'].bind('<Double-Button-1>', command)
    
    def get_listbox_select(self, event):
        # 获取当前选中的item
        cur_item = self.children['member_listbox'].curselection()
        # 获取当前选中的用户名
        user = self.user_list[len(self.user_list) - 1 - cur_item[0]]
        # print(user)
        return user
    
        
    def set_title(self, title):
        self.title(title)
        
    def on_send_click(self, command):
        self.children['sent_button']['command']=command
    
    def get_input(self):
        return self.children['input_area'].get('0.0', 'end')
    
    def clear_input(self):
        self.children['input_area'].delete('0.0', 'end')
        
    def clear_chat_area(self):
        self.children['chat_area'].delete('0.0', 'end')
    
    def append_msg(self, sender, msg, sent_time):
        # sent_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s:%s\n' %(sender, sent_time)
        self.children['chat_area'].insert('end',send_info,'blue')
        self.children['chat_area'].insert('end','  '+ msg +'\n')
        self.children['chat_area'].see('end')
    
    
    def append_system_msg(self, msg):
        set_info = '---%s---\n' %msg
        self.children['chat_area'].insert('end',' '*(52-len(msg))+ set_info,'system')
        self.children['chat_area'].see('end')
    
    def append_my_msg(self,sender,msg,sent_time):
        # sent_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s:%s\n' %(sender, sent_time)
        self.children['chat_area'].insert('end',send_info,'green')
        self.children['chat_area'].insert('end','  '+ msg +'\n')
        self.children['chat_area'].see('end')
        
    
    
    def on_window_close(self, command):
        self.protocol('WM_DELETE_WINDOW', command)
    
if __name__ == '__main__':
    chat = Chat()
    chat.append_system_msg('欢迎')
    print(type(strftime('%Y-%m-%d %H:%M:%S', localtime(time()))))
    chat.mainloop()