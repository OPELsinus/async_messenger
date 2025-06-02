from sqlalchemy import select

from app.models import Chat, ChatMember, Users
from app.db import get_db


class ChatRepository:
    def create_chat(self, is_group: bool, chat_name: str, db):
        chat = Chat(is_group=is_group, chat_name=chat_name)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def add_member(self, chat_id: str, user_id: int, db):
        print('Adding new members to', chat_id, user_id)
        member = ChatMember(chat_id=chat_id, user_id=user_id)
        db.add(member)
        db.commit()
        return member

    def get_raw_chats(self, user_id: int, db):
        return db.query(ChatMember).filter(ChatMember.user_id == user_id).all()

    def get_chats(self, all_chats: list, db):
        return db.query(Chat).filter(Chat.id.in_(all_chats)).all()

    def get_chat_id_for_current_user(self, current_user_id: int, companion_id: str, db):
        st1 = select(ChatMember.chat_id).where(ChatMember.user_id == current_user_id)
        st2 = select(ChatMember.chat_id).where(ChatMember.user_id == companion_id)

        chat_id = db.execute(st1.intersect(st2)).fetchone()
        if chat_id is None:
            return None
        return db.query(Chat).filter(Chat.id == chat_id[0]).first()

    def get_companions_for_chat_ids(self, chat_ids: list, db, current_user_id: int):

        members = db.query(ChatMember).filter(ChatMember.chat_id.in_(chat_ids)).all()
        companion_ids = {m.chat_id: m.user_id for m in members if m.user_id != current_user_id}

        user_ids = list(set(companion_ids.values()))
        users = db.query(Users).filter(Users.id.in_(user_ids)).all()
        user_map = {user.id: user.name for user in users}

        companions_map = {}
        for chat_id, user_id in companion_ids.items():
            companions_map[chat_id] = {'chat_name': user_map.get(user_id, "Unknown"), 'user_id': user_id}

        return companions_map


