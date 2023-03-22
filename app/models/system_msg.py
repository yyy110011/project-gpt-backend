


class SystemMsg:
    def __init__(self, db) -> None:
        self.db = db

    def add(self, category_id, name, message):
        category_id = int(category_id)
        category_id = category_id if category_id >= 1 else 1
        ret = self.db.fetch('''INSERT INTO public.system_msg(
            category_id, name, message)
            VALUES ($1, $2, $3) RETURNING *;''', category_id, name, message)
        return ret

    def get(self, id = 0):
        id = int(id)
        ret = self.db.fetch('SELECT * FROM system_msg WHERE system_msg.id=$1', id if id >= 1 else 1)
        return ret