import datetime

class Users:
    def __init__(self, db) -> None:
        self.db = db

    def create_user(self, name):
        ret = self.db.fetch('''INSERT INTO public.users(
            name, created_at)
            VALUES ($1, CURRENT_TIMESTAMP) RETURNING *;''', name)
        return ret
    
    def delete_user(self, user_id):
        ret = self.db.fetch('''DELETE FROM public.users
                WHERE id = $1 RETURNING *;''', int(user_id))
        return ret

    def get_users(self):
        ret = self.db.fetch('SELECT * FROM users')
        return ret

    def get_user_by_id(self, user_id):
        ret = self.db.fetch('SELECT * FROM users where users.id=$1', user_id)
        return ret