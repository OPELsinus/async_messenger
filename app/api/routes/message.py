import datetime

from fastapi import APIRouter, Depends
from app.db import get_db
from app.schemas.request_body import SendMessageRequest
from app.services.chat_service import ChatService
from app.services.message_service import MessageService
from app.services.user_service import UserService
from fastapi.responses import JSONResponse


router = APIRouter()
service = MessageService()
user_service = UserService()
chat_service = ChatService()


@router.get("/chats/{chat_id}/messages/")
def get_messages(chat_id: str, db=Depends(get_db)):
    messages = service.get_messages(chat_id, db)
    results = []
    for message in messages:
        user = user_service.repository.get_user_by_id(message.sender_id, db)
        timest = message.timestamp + datetime.timedelta(hours=5)
        results.append({
            'message_id': message.id,
            'sender_id': message.sender_id,
            'user_name': user.name,
            'text': message.text,
            'timestamp': datetime.datetime.strftime(timest, '%d.%m.%Y %H:%M:%S'),
            'is_read': message.is_read
        })
    return results


@router.post("/chats/messages/")
def send_message(message: SendMessageRequest, db=Depends(get_db)):
    print('OPUS')
    if message.chat_id is None or message.chat_id == '':
        new_chat_id = chat_service.create_chat(is_group=False, chat_name='', db=db)
        chat_service.add_member(new_chat_id.id, message.sender_id, db)
        chat_service.add_member(new_chat_id.id, message.receiver_id, db)
        message.chat_id = new_chat_id.id

    service.send_message(message.dict(), db)

    return JSONResponse({
        "chat_id": message.chat_id
    })
