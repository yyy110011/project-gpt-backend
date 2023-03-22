import asyncio
import asyncpg
from app.database import Database
from app.models.models import Models

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from .api_items import *


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


# Users

@app.get("/v1/users/", tags=["user"])
async def get_users():
    ret = await app.state.data_model.Users().get_users()
    return ret

@app.get("/v1/users/{user_id}", tags=["user"])
async def get_user(user_id: int):
    ret = await app.state.data_model.Users().get_user(user_id)
    return ret

@app.delete("/v1/users/{user_id}", tags=["user"])
async def delete_user(user_id: int):
    ret = await app.state.data_model.Users().delete_user(user_id)
    return ret

@app.put("/v1/users/", tags=["user"])
async def create_user(user: User):
    ret = await app.state.data_model.Users().create_user(user)
    return ret


# Chats

# Get chat list of particular user
@app.get("/v1/chats/{user_id}", tags=["chat"])
async def get_chats_list(user_id: int):
    ret = await app.state.data_model.Chats().get_chats(user_id)
    return ret

# Get chat info
@app.get("/v1/chats/{chat_id}", tags=["chat"])
async def get_chat(chat_id: int):
    ret = await app.state.data_model.Chats().get_chat(chat_id)
    return ret

# POST endpoint for adding a new chat
@app.post("/v1/chats", tags=["chat"])
async def create_chat(request: CreateChatRequest):
    chat_model = app.state.data_model.Chats()
    ret = await chat_model.new_chat(request.user_id, request.chat_name, request.system_msg_id)
    return ret

@app.put("/v1/chats/{chat_id}", tags=["chat"])
async def rename_chat(chat_id: int, chat_name: str):
    ret = await app.state.data_model.Chats().rename_chat(chat_id, chat_name)
    return ret

@app.delete("/v1/chats/{chat_id}", tags=["chat"])
async def delete_chat(chat_id: int):
    del_msg_ret = await app.state.data_model.Messages().delete_chat_message(chat_id)
    del_chat_ret = await app.state.data_model.Chats().delete_chat(chat_id)
    return del_chat_ret + del_msg_ret


# Messages

# POST endpoint for adding a new message to a chat
@app.post("/v1/chats/{chat_id}/messages", tags=["message"])
async def add_message(chat_id: int, request: MessageRequest):
    messages_model = app.state.data_model.Messages()
    chat_model = app.state.data_model.Chats()

    # Get msg count
    await chat_model.increase_chat_message_count(chat_id)
    ret = await messages_model.add_message(chat_id, "user", request.message)
    return ret

# PUT endpoint for updating an existing message in a chat
@app.put("/v1/chats/{chat_id}/messages/{message_id}", tags=["message"])
async def update_message(chat_id: int, message_id: int, request: MessageRequest):
    messages_model = app.state.data_model.Messages()
    ret = await messages_model.update_message(message_id, request.message)
    return ret

@app.post("/v1/generate", tags=["chatgpt"])
async def generate_result(message_sets: MessageSets):
    message_sets = [{"role": m.role, "content": m.content} for m in message_sets.message]
    return StreamingResponse(do_streaming_request(message_sets))

async def do_streaming_request(messages):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
    res_msg = ""
    res_role = ""
    for chunk in res:
        msg = ""
        if chunk["choices"][0]["delta"].get("role"):
            res_role = chunk["choices"][0]["delta"]["role"]
        if chunk["choices"][0]["delta"].get("content"):
            msg = chunk["choices"][0]["delta"]["content"]
            res_msg += msg
        yield msg
    # ret = await app.state.data_model.Messages().add_message(chat_id, "assistant", res_msg, counter)
    

