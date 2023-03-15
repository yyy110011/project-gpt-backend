from fastapi import FastAPI
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

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/v1/get_users/")
async def get_users():
    return user_db

@app.delete("/v1/delete_user/{user_id}")
async def delete_user(user_id: str):
    if user_db.get(user_id):
        user_db.pop(user_id)

@app.post("/v1/create_user/")
async def create_user(user_info: UserInfo):
    if not user_db.get(user_info.user_id):
        user_db[user_info.user_id] = str(user_info.user_name)
        return {"message": "Create fail.", "result": user_db}
    else:
        return {"message": "Create fail."}

@app.post("/v1/chat/")
async def chat(chat_message: ChatMessage):
    user_id = chat_message.user_id
    chat_id = chat_message.chat_id
    if varify_user(user_id):
        if not varify_chat(user_id, chat_id):
            chat_message_db[user_id][chat_id] = []

        print(chat_message.message)
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": chat_message.message}]
        )
        print(chat_message)
        return res["choices"][0]["message"]["content"]
    else:
        return "User not exist."

def varify_chat(user_id, chat_id):
    if chat_message_db[user_id].get(chat_id):
        return True
    return False
def varify_user(user_id):
    if user_db.get(user_id):
        return True
    return False
    

