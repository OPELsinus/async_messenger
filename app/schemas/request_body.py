from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    text: str
    timestamp: datetime
    is_read: bool


class UserRegistration(BaseModel):
    name: str
    nickname: str
    login: str
    password: str
    phone_number: str


class UserLogin(BaseModel):
    login: str
    password: str


class SendMessageRequest(BaseModel):
    chat_id: str
    sender_id: str
    receiver_id: str
    text: str
