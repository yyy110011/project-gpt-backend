from pydantic import BaseModel

class User(BaseModel):
    name: str

class ChatMessage(BaseModel):
    message: str