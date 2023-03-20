import asyncio
import asyncpg
from app.database import Database
from app.models.models import Models

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from .api_items import ChatMessage, UserInfo, user_db, chat_message_db


import openai
openai.organization = "org-WE8sJZEE7ZJuLyym6HyXaKDZ"
openai.api_key = "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"  #os.getenv("")


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


from .env import *
@app.on_event("startup")
async def startup_event():
    app.state.db = Database(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        host=DB_HOST,
        port=DB_PORT
    )
    app.state.data_model = Models(app.state.db)
    await app.state.db.connect()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/v1/get_users/", tags=["user"])
async def get_users():
    ret = await app.state.data_model.Users().get_users()
    return ret

@app.delete("/v1/delete_user/{user_id}", tags=["user"])
async def delete_user(user_id: str):
    ret = await app.state.data_model.Users().delete_user(user_id)
    return ret

@app.post("/v1/create_user/", tags=["user"])
async def create_user(user_info: UserInfo):
    ret = await app.state.data_model.Users().create_user(user_info.user_name)
    return ret
    # if not user_db.get(user_info.user_id):
    #     user_db[user_info.user_id] = str(user_info.user_name)
    #     chat_message_db[user_info.user_id] = {}
    #     return {"message": "Create fail.", "result": user_db}
    # else:
    #     return {"message": "Create fail."}

@app.delete("/v1/delete_chat/{user_id}_{chat_id}", tags=["chat"])
async def delete_chat(user_id, chat_id):
    if verify_chat(user_id, chat_id):
        chat_message_db[user_id].pop(chat_id)

@app.get("/v1/get_chats/{user_id}", tags=["chat"])
async def get_chats(user_id):
    return list(chat_message_db[user_id].keys())

@app.get("/v1/chat/{user_id}_{chat_id}", tags=["chat"])
async def get_chat(user_id, chat_id):
    if verify_user(user_id):
        if verify_chat(user_id, chat_id):
            return chat_message_db[user_id][chat_id]

@app.post("/v1/chat/", tags=["chat"])
async def chat(chat_message: ChatMessage):
    user_id = chat_message.user_id
    chat_id = chat_message.chat_id
    if verify_user(user_id):
        if not verify_chat(user_id, chat_id):
            chat_message_db[user_id][chat_id] = [{"role": "system", "content": "You are a AI assistant."}]

        chat_message_db[user_id][chat_id].append(gen_message_dict(chat_message.message))

        return StreamingResponse(do_streaming_requese(chat_message_db, user_id, chat_id))
    else:
        return "User not exist."

def do_streaming_requese(chat_message_db, user_id, chat_id):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_message_db[user_id][chat_id],
        stream=True
    )
    res_msg = ""
    res_role = ""
    for chunk in res:
        msg = ""
        if chunk["choices"][0]["delta"].get("role"):
            res_role = chunk["choices"][0]["delta"]["role"]
            chat_message_db[user_id][chat_id].append(
                {
                    "role": res_role,
                    "content": res_msg
                }
            )
        if chunk["choices"][0]["delta"].get("content"):
            msg = chunk["choices"][0]["delta"]["content"]
            chat_message_db[user_id][chat_id][-1]["content"] += msg
            # res_msg += msg
        yield msg
    

def gen_message_dict(message):
    return {"role": "user", "content": message}

def verify_chat(user_id, chat_id):
    if chat_message_db[user_id].get(chat_id):
        return True
    return False
def verify_user(user_id):
    if user_db.get(user_id):
        return True
    return False
    

