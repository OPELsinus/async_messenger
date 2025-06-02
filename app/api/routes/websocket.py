import json
import uuid
import asyncio
from typing import Dict, Set, DefaultDict
from collections import defaultdict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.db import get_db
from app.services.message_service import MessageService

router = APIRouter()
message_service = MessageService()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_chats: DefaultDict[int, Set[int]] = defaultdict(set)  # user_id -> set of chat_ids
        self.chat_users: DefaultDict[str, Set[str]] = defaultdict(set)  # chat_id -> set of user_ids

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            for chat_id in self.user_chats.get(user_id, set()):
                self.chat_users[chat_id].discard(user_id)
            self.user_chats.pop(user_id, None)
            self.active_connections.pop(user_id, None)

    async def join_chat(self, user_id: int, chat_id: str):
        self.user_chats[user_id].add(chat_id)
        self.chat_users[chat_id].add(user_id)

    async def broadcast(self, message: dict, chat_id: str, exclude_user_id: int = None):
        for user_id in self.chat_users.get(chat_id, set()):
            if user_id != exclude_user_id and user_id in self.active_connections:
                try:
                    await self.active_connections[user_id].send_json(message)
                except:
                    # Handle disconnected users
                    self.disconnect(user_id)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db=Depends(get_db)):
    await manager.connect(websocket, user_id)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=30.0)

                if data["type"] == "join_chat":
                    await manager.join_chat(user_id, data["chat_id"])
                elif data["type"] == "send_message":
                    message_data = {
                        "id": str(uuid.uuid4()),
                        "chat_id": data["chat_id"],
                        "sender_id": user_id,
                        "text": data["text"]
                    }
                    message = message_service.send_message(message_data, db)
                    await manager.broadcast({
                        "type": "new_message",
                        "message": message.dict()
                    }, data["chat_id"], user_id)

            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                try:
                    await websocket.send_json({"type": "ping"})
                except:
                    break  # Connection is dead
            except json.JSONDecodeError:
                continue  # Ignore invalid JSON

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {str(e)}")
    finally:
        manager.disconnect(user_id)