import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(50))
    login: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(256))
    phone_number: Mapped[str] = mapped_column(String(14))


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_name: Mapped[str] = mapped_column(String)
    is_group: Mapped[bool] = mapped_column(Boolean, default=False)


class ChatMember(Base):
    __tablename__ = "chat_members"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id: Mapped[str] = mapped_column(String, ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))


class MessageDB(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id: Mapped[str] = mapped_column(String, ForeignKey("chats.id"))
    sender_id: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
