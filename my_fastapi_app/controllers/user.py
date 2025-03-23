from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models.database import get_db
from models.user import User
from services.user_service import get_all_users, save_user, get_user_by_id, delete_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@router.get("/users/list", response_class=HTMLResponse)
async def get_user_list(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse("components/user_list.html", {"request": request, "users": users})

@router.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    return templates.TemplateResponse("components/user_form.html", {"request": request, "user": user})

@router.post("/users/save", response_class=HTMLResponse)
async def save_user_form(request: Request, id: int = Form(None), name: str = Form(...), db: Session = Depends(get_db)):
    if not name:
        raise HTTPException(status_code=422, detail="Name is required")
    if id:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = name
    else:
        user = User(name=name)
        db.add(user)
    db.commit()
    users = db.query(User).all()
    return templates.TemplateResponse("components/user_list.html", {"request": request, "users": users})

@router.delete("/users/delete/{user_id}", response_class=HTMLResponse)
async def delete_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    users = get_all_users(db)
    return templates.TemplateResponse("components/user_list.html", {"request": request, "users": users})

@router.get("/users/new", response_class=HTMLResponse)
async def new_user_form(request: Request):
    return templates.TemplateResponse("components/user_form.html", {"request": request, "user": None})
