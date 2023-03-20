

class Chats:
    def __init__(self, db) -> None:
        self.db = db

    def get_chats(self, user_id):
        ret = self.db.fetch('SELECT * FROM chats WHERE chats.user_id=$1', user_id)
        return ret

    def get_chat_info(self, chat_id):
        ret = self.db.fetchrow('SELECT * FROM chats where chats.id=$1', chat_id)
        return ret