from app.repositories.chat_repository import ChatRepository
from app.services.user_service import UserService
from app.settings.config import settings

user_service = UserService()

class ChatService:
    def __init__(self):
        self.repository = ChatRepository()

    def create_chat(self, is_group: bool, chat_name: str, db):
        return self.repository.create_chat(is_group, chat_name, db)

    def add_member(self, chat_id: str, user_id: str, db):
        return self.repository.add_member(chat_id, user_id, db)

    def get_chats_for_user(self, user_id: str, db):
        raw_memberships = self.repository.get_raw_chats(user_id, db)
        chat_ids = [cm.chat_id for cm in raw_memberships]

        chat_data = self.repository.get_chats(chat_ids, db)
        companions_map = self.repository.get_companions_for_chat_ids(chat_ids, db, user_id)
        user_chats = []

        for chat in chat_data:
            if chat.is_group:
                chat_display_name = chat.chat_name
                name = None
            else:
                name = companions_map.get(chat.id, {'chat_name': "Unknown"}).get('chat_name')
                chat_display_name = name

            user_id = companions_map.get(chat.id, {'user_id': settings.ADMIN_ID}).get('user_id')

            user_nickname = user_service.get_user_by_id(user_id, db).nickname

            user_chats.append({
                "id": chat.id,
                "chat_name": chat_display_name,
                "is_group": chat.is_group,
                "user_id": user_id,
                "user_nickname": user_nickname,
                "name": name
            })

        return user_chats

    def get_chat_id(self, current_user_id: str, companion_id: str, db):
        return self.repository.get_chat_id_for_current_user(current_user_id, companion_id, db)
