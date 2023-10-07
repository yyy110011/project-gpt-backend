from .users import Users
from .chats import Chats
from .messages import Messages
from .system_msg import SystemMsg


class Models:
    def __init__(self, db) -> None:
        self.db = db
        self.users = None
        self.chats = None
        self.messages = None
        self.system_msg = None

    def Users(self):
        if not self.users:
            self.users = Users(self.db)
        return self.users

    def Chats(self):
        if not self.chats:
            self.chats = Chats(self.db)
        return self.chats
    
    def Messages(self):
        if not self.messages:
            self.messages = Messages(self.db)
        return self.messages
    
    def SystemMsg(self):
        if not self.system_msg:
            self.system_msg = SystemMsg(self.db)
        return self.system_msg