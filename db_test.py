
import asyncio
import asyncpg

# async def main():
#     conn = await asyncpg.connect(user='postgres', password='admin',
#                                  database='postgres', host='ec2-54-248-212-218.ap-northeast-1.compute.amazonaws.com', port=5487)
#     values = await conn.fetch(
#         'SELECT chats.name AS chats_name FROM chats JOIN users ON users.id = chats.user_id'
#     )
#     for i in values:
#         print(i['chats_name'])
#     await conn.close()

# asyncio.run(main())

from app.database import Database

db = Database(
    user='postgres',
    password='admin',
    database='postgres',
    host='ec2-54-248-212-218.ap-northeast-1.compute.amazonaws.com',
    port=5487
)

loop = asyncio.get_event_loop()
loop.run_until_complete(db.connect())

ret = loop.run_until_complete(db.fetch('SELECT chats.name AS chats_name FROM chats JOIN users ON users.id = chats.user_id')) 
print(ret)