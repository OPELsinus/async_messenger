from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_connections: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        for chat_id, users in self.chat_connections.items():
            if user_id in users:
                users.remove(user_id)

    async def join_chat(self, user_id: str, chat_id: str):
        if chat_id not in self.chat_connections:
            self.chat_connections[chat_id] = []
        if user_id not in self.chat_connections[chat_id]:
            self.chat_connections[chat_id].append(user_id)

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str, chat_id: str, sender_id: str):
        if chat_id in self.chat_connections:
            for user_id in self.chat_connections[chat_id]:
                if user_id != sender_id:
                    await self.send_personal_message(message, user_id)
