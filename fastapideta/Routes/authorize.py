from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import models, database
from Backend import Schema, Authenticate as Auth
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])
templates = Jinja2Templates(directory="Views")
db = database.get_db

@router.get('/signup', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def load_signup_page(request:Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_account(request:Schema.Create_Acc, db:Session = Depends(db)):
    existing_user = Auth.FindUser(request, db)
    if not existing_user:
        if request.role == 'admin':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Admin Account can not be created from here")
        new_user = Auth.AddUser(request, db)
        if type(new_user) == models.User:
            return new_user
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account was not created")
    else:
        return None

@router.get('/login', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def load_login_page(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(request:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(db)):
    access_token = Auth.Login(request, db)
    return access_token