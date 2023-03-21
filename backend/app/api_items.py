from pydantic import BaseModel

class UserInfo(BaseModel):
    user_name: str

class ChatMessage(BaseModel):
    message: str