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


from fastapi import status
from fastapi.responses import RedirectResponse
from app.settings.config import settings


@app.get("/")
async def read_root(request: Request, db=Depends(get_db)):
    user_id = int(request.session.get("user_id"))
    nickname = request.session.get("nickname")
    name = request.session.get("name")

    if not user_id:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    chat_service = ChatService()
    chats = chat_service.get_chats_for_user(user_id, db=db)

    admin_id = settings.ADMIN_ID

    personal_chat = None
    for c in chats:
        companion_id = c.get('user_id')
        if not c['is_group'] and companion_id == admin_id:
            personal_chat = c
            break

    if not personal_chat and user_id != admin_id:
        chat_exists = chat_service.get_chat_id(user_id, admin_id, db)
        if not chat_exists:
            chat = chat_service.create_chat(is_group=False, chat_name='', db=db)
            chat_service.add_member(chat.id, user_id, db)
            chat_service.add_member(chat.id, admin_id, db)
        else:
            chat = chat_exists

        chats_ = chat_service.get_chats_for_user(user_id, db=db)

        for c in chats_:
            if c['id'] == chat.id:
                personal_chat = c
                break

    selected_chat_id = personal_chat['id'] if personal_chat else None
    selected_chat_name = personal_chat['chat_name'] if personal_chat else "Main chat"
    selected_user_nickname = personal_chat['user_nickname'] if personal_chat else ''
    print(chats)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chats": chats,
        "nickname": nickname,
        "name": name,
        "selected_chat_id": selected_chat_id,
        "selected_chat_name": selected_chat_name,
        "selected_user_nickname": selected_user_nickname
    })
