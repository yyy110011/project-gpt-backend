from pydantic import BaseModel

class User(BaseModel):
    name: str

class CreateChatRequest(BaseModel):
    user_id: int
    chat_name: str
    system_msg_id: int

class MessageRequest(BaseModel):
    message: str

class MessageUnit(BaseModel):
    role: str
    content: str

class MessageSets(BaseModel):
    message: list[MessageUnit]