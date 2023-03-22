

class Chats:
    def __init__(self, db) -> None:
        self.db = db

    def new_chat(self, user_id, name, system_msg_id):
        ret = self.db.fetch('''INSERT INTO public.chats(
            user_id, name, system_msg_id)
            VALUES ($1, $2, $3) RETURNING *;''', user_id, name, system_msg_id if system_msg_id >= 1 else 1)
        return ret

    def rename_chat(self, chat_id, name):
        ret = self.db.fetch('''UPDATE public.chats
            SET name=$1
            WHERE chats.id=$2 RETURNING *;''', name, int(chat_id))
        return ret

    def update_chat_message_count(self, chat_id, count):
        ret = self.db.fetch('''UPDATE public.chats
            SET message_counts=$1
            WHERE chats.id=$2 RETURNING *;''', count + 1, int(chat_id))
        return ret
    
    async def increase_chat_message_count(self, chat_id):
        chat_info = await self.db.fetchrow('SELECT * FROM chats where chats.id=$1', chat_id)
        ret = await self.db.fetch('''UPDATE public.chats
            SET message_counts=$1
            WHERE chats.id=$2 RETURNING *;''', chat_info["message_counts"] + 1, int(chat_id))
        return ret

    def delete_chat(self, chat_id):
        ret = self.db.fetch('''DELETE FROM public.chats
                WHERE id = $1 RETURNING *;''', int(chat_id))
        return ret

    def get_chat_info(self, chat_id: int):
        ret = self.db.fetchrow('SELECT * FROM chats where chats.id=$1', chat_id)
        return ret

    def get_chat(self, chat_id: int):
        ret = self.db.fetch('SELECT * FROM chats WHERE chats.id=$1', chat_id)
        return ret

    def get_chats(self, user_id: int):
        ret = self.db.fetch('SELECT * FROM chats WHERE chats.user_id=$1', int(user_id))
        return ret