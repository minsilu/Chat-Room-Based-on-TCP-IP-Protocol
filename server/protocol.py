from config import *

class RespongeProtocol(object):

    @staticmethod
    def response_login(result, nickname, username):
        return DELIMITER.join([RESPONSE_LOGIN, result, nickname, username])

    @staticmethod
    def response_chat(nickname,message,fromwho,time):
        return DELIMITER.join([RESPONSE_CHAT, nickname, message,fromwho,time])
    
    @staticmethod
    def response_system(message,fromwho):
        return DELIMITER.join([SYSTEM_MESSAGE, message,fromwho])

    