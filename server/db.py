
from config import *
import pandas as pd

class DataBase(object):
    def __init__(self):
        self.users = pd.read_csv("database/user.csv")
        self.users["user_password"] = self.users["user_password"].astype(str)
        self.friends = pd.read_csv("database/friends.csv").astype(str)
        self.groups = pd.read_csv("database/groups.csv").astype(str)
        
    def get_one(self,user_name):
        data = self.users[self.users["user_name"]==user_name]
        if data.empty:
            return None
        else:
            return data.to_dict(orient="records")[0]
        
    def add_one(self,user_name,user_password,user_nickname):
        if user_name in self.users["user_name"].values:
            print("user_name already exists")
            return 0
        user_id=self.users["user_id"].max()+1
        self.users = self.users.append({"user_id":user_id,"user_name":user_name,"user_password":user_password,"user_nickname":user_nickname},ignore_index=True)
        self.users.to_csv("database/user.csv",index=False)
        
        
    def get_friends(self,user_name):
        # if user_name not in self.users["user_name"].values:
        #     print("user_name not exists")
        #     return 0
        data = self.friends[self.friends["user_name"]==user_name]
        if data.empty:
            return None
        else:
            return data["friend_name"].values.tolist()
        
        
    def add_friend(self,one,other):
        self.friends=self.friends.append({"user_name":one,"friend_name":other},ignore_index=True)
        self.friends=self.friends.append({"user_name":other,"friend_name":one},ignore_index=True)
        self.friends.to_csv("database/friends.csv",index=False)
        

    def delete_friend(self,one,other):
        self.friends.drop(self.friends[(self.friends["user_name"]==one) & (self.friends["friend_name"]==other)].index,inplace=True)
        self.friends.drop(self.friends[(self.friends["user_name"]==other) & (self.friends["friend_name"]==one)].index,inplace=True) 
        self.friends.to_csv("database/friends.csv",index=False)
        
    def get_groups(self,user_name):
        data = self.groups[self.groups["user_name"]==user_name]
        if data.empty:
            return None
        else:
            return data['group_name'].values.tolist()
        
    def get_group_members(self,group_name):
        data = self.groups[self.groups["group_name"]==group_name]
        if data.empty:
            return None
        else:
            return data["user_name"].values.tolist()
        

    def add_group(self,group_name,*user_names):
        if group_name in self.groups["group_name"].values:
            print("group_name already exists")
            return 0
        for user in user_names:
            self.groups = self.groups.append({"group_name":group_name,"user_name":user},ignore_index=True)
        # print(self.groups)
        self.groups.to_csv("database/groups.csv",index=False)
    
    def delete_group(self,group_name):
        if group_name not in self.groups["group_name"].values:
            print("group_name not exists")
            return 0
        self.groups.drop(self.groups[self.groups["group_name"]==group_name].index,inplace=True)
        self.groups.to_csv("database/groups.csv",index=False)
    

    def join_group(self,user_name,group_name):
        if group_name not in self.groups["group_name"].values:
            print("group_name not exists")
            return 0
        self.groups = self.groups.append({"group_name":group_name,"user_name":user_name},ignore_index=True)
        self.groups.to_csv("database/groups.csv",index=False)
        
    def exit_group(self,user_name,group_name):
        if group_name not in self.groups["group_name"].values:
            print("group_name not exists")
            return 0
        self.groups.drop(self.groups[(self.groups["user_name"]==user_name) & (self.groups["group_name"]==group_name)].index,inplace=True)
        self.groups.to_csv("database/groups.csv",index=False)
        
    
# class DataBase(object):
#     def __init__(self):
#         self.conn = connect(host=DB_HOST, port=DB_PORT, user=DB_USER, 
#                             password=DB_PASSWORD, database=DB_NAME)
#         self.cursor = self.conn.cursor()
        
#     def close(self):
#         self.cursor.close()
#         self.conn.close()
        
#     def get_one(self, sql):
#         self.cursor.execute(sql)
#         query_result = self.cursor.fetchone()
#         if not query_result:
#             return None
        
#         fileds = [field[0] for field in self.cursor.description]
#         return_data = {}
#         for field, value in zip(fileds, query_result):
#             return_data[field] = value
        
#         return return_data

if __name__ == '__main__':
    db = DataBase()
    # print(db.users)
    # data = db.get_one('1111')
    # print(data)
    # print(db.friends)
    # db.add_one('user6','666666','frank')
    # print(db.get_friends('user4'))
    # db.add_friend('user4','user3')
    # db.delete_friend('user4','user3')
    # print(db.friends)
    # print(db.get_groups('user1'))
    # print(db.get_group_members('home'))
    # print(db.get_groups('user1'))
    # print(db.get_group_members('group1'))
    # db.exit_group('user5','group2')
    db.join_group('user5','study')
    
