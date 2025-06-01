from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.chat_service import ChatService

router = APIRouter()
service = ChatService()


@router.post("/chats/")
def create_chat(is_group: bool, chat_name: str, db=Depends(get_db)):
    return service.create_chat(is_group, chat_name, db)

