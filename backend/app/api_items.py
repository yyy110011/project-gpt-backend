from pydantic import BaseModel

user_db = {
    "0": "test1"
}

# user name as key
chat_message_db = {
    "0":{
        "c++ programming": [
            {"role": "system", "content": "You are so good,"},
            {"role": "user", "content": "You are so good,"},
            {"role": "assistant", "content": "You are so good,"},
        ],
        "c++ 2": [
    
        ],
        "c++ 3": [
    
        ],
    },
    "2":{
        "c++ programming": [
    
        ],
        "c++ 2": [
    
        ],
        "c++ 3": [
    
        ],
    },
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