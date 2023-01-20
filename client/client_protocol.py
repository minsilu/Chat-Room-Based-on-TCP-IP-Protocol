from config import *
from time import strftime, localtime, time

class RespongeProtocol(object):

    @staticmethod
    def request_login(username, password):
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat(username, message):
        return DELIMITER.join([REQUEST_CHAT, username, message])
    
    @staticmethod
    def request_onechat(username, message, towho):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        return DELIMITER.join([REQUEST_CHAT, username, message, towho, TO_ONE, send_time])
    
    @staticmethod
    def request_groupchat(username, message, towho):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        return DELIMITER.join([REQUEST_CHAT, username, message,towho, TO_GROUP, send_time])
    
    @staticmethod
    def request_groupenter(username, message, towho):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        return DELIMITER.join([REQUEST_CHAT, username, message,towho, ENTER_ROOM, send_time])
    
    @staticmethod
    def request_groupexit(username, message, towho):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        return DELIMITER.join([REQUEST_CHAT, username, message,towho, EXIT_ROOM, send_time])
