from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Profile, Authenticate as Auth

router = APIRouter( prefix='/profile', tags=['Profile'])
templates = Jinja2Templates(directory="Views")
db = database.get_db

@router.get("/", status_code=status.HTTP_200_OK)
def redirect_to_profile(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse(f'{current_user.username}')

@router.get("/{username}", response_class=HTMLResponse, response_model=Schema.Profile, status_code=status.HTTP_200_OK)
def profile(request:Request, username:str, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session = Depends(db)):
    user = Profile.Display_Profile(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No Data available for {username}")
    else:
        # return user # remove response_class from the decorator
        return templates.TemplateResponse("profile.html", {"request": request, "data":user, "user":current_user.user})
    