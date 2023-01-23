from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import Schema
from Database import models

def All_Profile(db : Session):
    profiles = db.query(models.User).all()
    result = [Schema.Profile(name=p.name, usn=p.usn, email=p.email, dob=str(p.dob), role=p.role) for p in profiles]
    return result

def Delete_Profile(data:str, db:Session):
    try:
        profile = db.query(models.User).filter(models.User.usn == data.lower())
        if not profile.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such user found")
        profile.delete(synchronize_session=False)
        db.commit()
        return {"status":"Successful", "data":data}
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Profile not deleted due to following error {e}")

def All_Game(db : Session):
    games = db.query(models.Game).all()
    result = [Schema.Game(game_id=g.g_id, game_name=g.g_name, game_type=g.g_type) for g in games]
    return result

def Add_Game(data:Schema.Add_Game, db: Session):
    try:
        game = db.query(models.Game).filter(models.Game.g_name == data.name.lower()).first()
        if game:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game already exists")
        new_game = models.Game(g_name=data.name.lower(), g_type=data.type)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"game not added due to following error {e}")

def Delete_Game(data:int, db:Session):
    try:
        game = db.query(models.Game).filter(models.Game.g_id == data)
        if not game.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such game found")
        game.delete(synchronize_session=False)
        db.commit()
        return {"status":"Successful", "data":data}
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game not deleted due to following error {e}")

def All_Coach(db : Session):
    profiles = db.query(models.User).filter(models.User.role == 'coach').all()
    result = [Schema.Profile(name=p.name, usn=p.usn, email=p.email, dob=str(p.dob), role=p.role) for p in profiles]
    return result

def Add_Tournament(data: Schema.Add_Tournament,db : Session):
    try:
        new_tournament = models.Tournament(t_name=data.name, t_desc=data.description, t_date=data.date, last_reg_date=data.last_reg_date, coach=data.coach, game=data.game)
        db.add(new_tournament)
        db.commit()
        db.refresh(new_tournament)
        return new_tournament
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tournament not registered due to {e}")

def Delete_Tournament(data:int, db:Session):
    try:
        tournament = db.query(models.Tournament).filter(models.Tournament.t_id == data)
        if not tournament.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such tournament found")
        tournament.delete(synchronize_session=False)
        db.commit()
        return {"status":"Successful", "data":data}
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tournament not deleted due to following error {e}")