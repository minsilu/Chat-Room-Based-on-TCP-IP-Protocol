from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import Button


class Login(Tk):
    def __init__(self):
        super(Login,self).__init__()
        
        # 窗口属性
        self.window_init()
        self.add_widgets()
        self.on_reset_click(lambda : print('reset'))
        self.on_login_click(lambda : print('login'))
    

    
    def window_init(self):
            self.title('登录')
            
            window_width = 255
            window_height = 95
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            pos_x = (screen_width - window_width) // 2
            pos_y = (screen_height - window_height) // 2
            self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))
            
            self.resizable(0, 0)
            
            
    def add_widgets(self):
        username_label = Label(self, text='用户名：')
        username_label.grid(row=0, column=0, padx=10, pady=5)
        
        username_entry = Entry(self,name='username_entry', width=25)
        username_entry.grid(row=0, column=1)
        
        password_label = Label(self, text='密码：')
        password_label.grid(row=1, column=0, padx=10, pady=5)
        
        password_entry = Entry(self,name='password_entry', width=25, show='*')
        password_entry.grid(row=1, column=1)
        
        butto_frame = Frame(self,name='button_frame')
        reset_button = Button(butto_frame, text=' 重置 ', name='reset_button')
        reset_button.pack(side='left', padx=20)
        login_button = Button(butto_frame, text=' 登录 ', name='login_button')
        login_button.pack(side='left')
        butto_frame.grid(row=2, columnspan=2,pady=5)
        
    def get_username(self):
        return self.children['username_entry'].get()
    
    def get_password(self):
        return self.children['password_entry'].get()
    
    def clear_username(self):
        self.children['username_entry'].delete(0,'end')
        
    def clear_password(self):
        self.children['password_entry'].delete(0,'end')
        
    def on_reset_click(self,command):
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command
        
    def on_login_click(self,command):
        login_button = self.children['button_frame'].children['login_button']
        login_button['command'] = command
    
    def on_window_close(self,command):
        self.protocol('WM_DELETE_WINDOW',command)
    
if __name__ == '__main__':
    window = Login()
    window.mainloop()