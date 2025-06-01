from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self):
        self.repository = MessageRepository()

    def get_messages(self, chat_id: str, db):
        return self.repository.get_messages(chat_id, db)

    def send_message(self, message_data: dict, db):
        return self.repository.create_message(message_data, db)

    def mark_as_read(self, message_id: str, db):
        return self.repository.mark_as_read(message_id, db)

