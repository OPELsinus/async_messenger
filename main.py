from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from app.api.routes import chat, message, websocket, user
from app.db import get_db
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.services.chat_service import ChatService
from app.settings.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(message.router)
app.include_router(websocket.router)


@app.get("/")
async def read_root(request: Request, db=Depends(get_db)):
    user_id = request.session.get("user_id")
    nickname = request.session.get("nickname")
    name = request.session.get("name")

    if not user_id:
        return RedirectResponse("/login", 303)

    chat_service = ChatService()
    chats = chat_service.get_chats_for_user(user_id, db=db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chats": chats,
        "nickname": nickname,
        "name": name
    })

