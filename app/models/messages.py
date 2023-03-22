
class Messages:
    def __init__(self, db) -> None:
        self.db = db

    def add_message(self, chat_id, role, message):
        ret = self.db.fetch('''INSERT INTO public.messages(
            chat_id, role, message)
            VALUES ($1, $2, $3) RETURNING *;''', chat_id, role, message)
        return ret

    def get_messages(self, chat_id):
        ret = self.db.fetch('SELECT * FROM messages WHERE messages.chat_id=$1', int(chat_id))
        return ret

    def delete_chat_message(self, chat_id):
        ret = self.db.fetch('''DELETE FROM public.messages
            WHERE chat_id = $1 RETURNING *;''', int(chat_id))
        return ret
    
    def update_message(self, message_id, message):
        ret = self.db.fetch('''UPDATE public.messages
            SET message=$1
            WHERE messages.id=$2 RETURNING *;''', message, message_id)
        return ret