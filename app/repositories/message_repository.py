from app.models import MessageDB, Users


class MessageRepository:
    def get_messages(self, chat_id: str, db):
        return db.query(MessageDB).filter(MessageDB.chat_id == chat_id).order_by(MessageDB.timestamp).all()

    def create_message(self, message_data: dict, db):
        message = MessageDB(chat_id=message_data['chat_id'], sender_id=message_data['sender_id'], text=message_data['text'])
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def mark_as_read(self, message_id: str, db):
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if message:
            message.is_read = True
            db.commit()
            return message
        return None
