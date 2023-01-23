from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Admin, Authenticate as Auth
from typing import List

router = APIRouter( prefix='/admin', tags=['Admin'])
templates = Jinja2Templates(directory="Views/Admin")
db = database.get_db

## <<<--------Admin Dashboard-------->>>
@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def admin_dashboard(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    if current_user.user == 'admin':
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

## <<<--------User Profile Section-------->>>
@router.get("/profile", response_class=HTMLResponse, response_model=List[Schema.Profile], status_code=status.HTTP_200_OK)
def profile(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        profile = Admin.All_Profile(db)
        # return profile # remove response_class from decorator
        return templates.TemplateResponse("profile.html", {"request":request, "data":profile})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.get("/select_profile", status_code=status.HTTP_200_OK)
def redirect_to_profile(username:str, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse(f'/profile/{username}')

@router.delete("/profile", status_code=status.HTTP_202_ACCEPTED)
def delete_profile(username:str, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        if username == current_user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin account cannot be deleted")
        profile = Admin.Delete_Profile(username, db)
        return {"data":profile, "status":"Successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

## <<<--------Game Section-------->>>
@router.get("/game", response_class=HTMLResponse, response_model=List[Schema.Game], status_code=status.HTTP_200_OK)
def game(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        game = Admin.All_Game(db)
        # return game # remove response_class from decorator
        return templates.TemplateResponse("game.html", {"request":request, "data":game})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.get("/addgame", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def add_game_page(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        return templates.TemplateResponse("addgame.html", {"request":request})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.post("/addgame", status_code=status.HTTP_200_OK)
def add_game(request:Schema.Add_Game, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        game = Admin.Add_Game(request, db)
        if not game:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game not Updated")
        else:
            return game
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.delete("/game", status_code=status.HTTP_202_ACCEPTED)
def delete_game(game:int, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        game = Admin.Delete_Game(game, db)
        return {"data":game, "status":"Successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

## <<<--------Tournament Section-------->>>
@router.get("/tournament", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def tournament(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        RedirectResponse('/tournament')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.get("/select_tournament", status_code=status.HTTP_200_OK)
def redirect_to_tournament(id:int, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse(f'/tournament/{id}')

@router.get("/addtournament",response_class=HTMLResponse, response_model=Schema.Game, status_code=status.HTTP_200_OK)
def add_tournament_page(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        coach = Admin.All_Coach(db)
        game = Admin.All_Game(db)
        return templates.TemplateResponse("addtournament.html", {"request":request, "coach":coach, "game":game})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.post("/addtournament", status_code=status.HTTP_200_OK)
def add_tournament(request:Schema.Add_Tournament, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        new_tournament = Admin.Add_Tournament(request, db)
        return {"data":new_tournament, "status":"Successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

@router.delete("/tournament", status_code=status.HTTP_202_ACCEPTED)
def delete_tournament(tournament:int, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    if current_user.user == 'admin':
        tournament = Admin.Delete_Tournament(tournament, db)
        return {"data":tournament, "status":"Successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")