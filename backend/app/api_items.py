from pydantic import BaseModel

user_db = {
    "0": "test1"
}

chat_message_db = {
    "0":{
    }
}

sim_db = {
    
}

class UserInfo(BaseModel):
    user_id: str
    user_name: str

class ChatMessage(BaseModel):
    user_id: str
    user_name: str
    chat_id: str
    message: str