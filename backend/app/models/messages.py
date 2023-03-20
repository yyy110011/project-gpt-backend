
class Messages:
    def __init__(self, db) -> None:
        self.db = db

    def get_messages(self, chat_id):
        ret = self.db.fetch('SELECT * FROM messages WHERE messages.chat_id=$1', chat_id)
        return ret[0]
