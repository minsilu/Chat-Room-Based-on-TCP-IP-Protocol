from database.db import DataBase

db=DataBase()
while True:
    s =input('请选择操作\n 1.注册\n 2.修改用户数据 \n 3.退出\n')
    if s=='1':
        user_name=input('请输入用户名')
        user_password=input('请输入密码')
        user_nickname=input('请输入昵称')
        db.add_one(user_name,user_password,user_nickname)
        print('注册成功')
    if s=='2':
        user_name=input('请输入用户名')
        if user_name not in db.users["user_name"].values:
            print('用户名不存在')
            continue
        while True:
            m=input('请选择操作: \n 1.退出 \n 2.增加好友 \n 3.删除好友 \n 4.加群 \n 5.退群 \n 6.创建群聊 \n 7.删除群聊 \n 8.注销用户\n')
            if m=='1':
                break
            if m=='2':
                friend_name=input('请输入用户名')
                db.add_friend(user_name,friend_name)
                print('添加成功')
            if m=='3':
                friend_name=input('请输入用户名')
                db.delete_friend(user_name,friend_name)
                print('删除成功')
            if m=='4':
                group_name=input('请输入群名')
                db.join_group(user_name,group_name)
                print('加群成功')
            if m=='5':
                group_name=input('请输入群名')
                db.exit_group(user_name,group_name)
                print('退群成功')
            if m=='6':
                group_name=input('请输入群名')
                db.add_group(group_name,user_name)
                print('创建成功')
            if m=='7':
                group_name=input('请输入群名')
                db.delete_group(group_name)
                print('删除成功')
            if m=='8':
                db.delete_user(user_name)
                print('注销成功')
    if s=='3':
        break







