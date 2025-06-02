from fastapi import APIRouter, Depends, Request, Form, Query
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.db import get_db
from app.schemas.request_body import UserRegistration, UserLogin
from app.services.chat_service import ChatService
from app.services.user_service import UserService
from app.settings.config import settings

router = APIRouter()
service = UserService()
chat_service = ChatService()

templates = Jinja2Templates(directory="app/templates")


@router.get("/registration")
def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/registration")
def registration_post(
    request: Request,
    name: str = Form(...),
    nickname: str = Form(...),
    login: str = Form(...),
    password: str = Form(...),
    phone_number: str = Form(...),
    db=Depends(get_db)
):
    user_body = UserRegistration(name=name, nickname=nickname, login=login, password=password, phone_number=phone_number)
    user_exists = service.check_if_user_exists(login, db)
    if not user_exists:
        new_user = service.create_user(user_body, db)

        chat = chat_service.create_chat(is_group=False, chat_name='', db=db)
        chat_service.add_member(chat.id, new_user.id, db)
        chat_service.add_member(chat.id, settings.ADMIN_ID, db)

        return RedirectResponse("/", 303)
    return templates.TemplateResponse("registration.html", {"request": request, "error": "User already exists"})


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_post(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    user_body = UserLogin(login=login, password=password)
    user = service.auth_user(user_body, db)
    if user:
        request.session["user_id"] = user.id
        request.session["nickname"] = user.nickname
        request.session["name"] = user.name
        return RedirectResponse("/", 303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)



@router.get("/api/search_users")
async def search_users(current_user_id: int, nickname: str = Query(...), db=Depends(get_db)):
    results = []
    all_satisfied_users = service.get_user_by_nickname(nickname, db)
    for user in all_satisfied_users:
        if user.id == current_user_id:
            continue
        result = chat_service.get_chat_id(current_user_id, user.id, db)
        results.append({
            "id": user.id,
            "name": user.name,
            "nickname": user.nickname,
            "chat_id": result.id if result is not None else None,
            "chat_name": result.chat_name if result is not None else None,
            "is_group": result.is_group if result is not None else False,
        })
    return results


@router.get("/download-db")
def download_db(request: Request):
    if request.session["user_id"] == 1:
        return FileResponse("app.db", media_type='application/octet-stream', filename="app.db")

    return RedirectResponse("/", 303)
