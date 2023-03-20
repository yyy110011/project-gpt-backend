from pydantic import BaseModel

class UserInfo(BaseModel):
    user_name: str

class ChatMessage(BaseModel):
    user_id: str
    user_name: str
    chat_id: str
    message: str