from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Tournament, Authenticate as Auth
from typing import List


router = APIRouter( prefix='/tournament', tags=['Tournament'])
templates = Jinja2Templates(directory="Views")
db = database.get_db

@router.get("/", response_class=HTMLResponse, response_model=List[Schema.Tournament], status_code=status.HTTP_200_OK)
def tournament(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    tournament = Tournament.All_Tournament(db)
    # return tournament # remove response_class from decorator
    return templates.TemplateResponse("tournament.html", {"request":request, "data":tournament})

@router.get("/{id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def tournament_profile(request:Request, id:int, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    detail = Tournament.Find_Tournament(id, db)
    registration = Tournament.Find_Registration(id, db)
    # return {"tournament":detail, "register":registration} # remove response_class
    return templates.TemplateResponse("tournament_profile.html", {"request":request, "tournament":detail, "register":registration})

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request:Request, id:int, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'player':
        new_register = Tournament.Add_Register(id, current_user.username, db)
        if not new_register:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration Got Over")
        else:
            return {"status":"Successfully", "data":new_register}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Players can register for Tournament")