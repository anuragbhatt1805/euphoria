from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import Schema
from Database import models
from datetime import datetime
def All_Tournament(db:Session):
    tournaments = db.query(models.Tournament, models.User, models.Game).join(models.Tournament.coach == models.User.usn).join(models.Tournament.game == models.Game.g_id).all()
    result = [Schema.Tournament(tour_id=t[0].t_id, name=t[0].t_name, description=t[0].t_desc, date=str(t[0].t_date), last_reg_date=str(t[0].last_reg_date), coach=Schema.Profile(name=t[1].name, usn=t[1].usn, email=t[1].email, dob=str(t[1].dob), role=t[1].role), game=Schema.Add_Game(name=t[2].g_name, type=t[2].g_type)) for t in tournaments]
    return result
def Find_Tournament(id:int, db:Session):
    t = db.query(models.Tournament, models.User, models.Game).join(models.Tournament.coach == models.User.usn).join(models.Tournament.game == models.Game.g_id).filter(models.Tournament.t_id == id).first()
    result = Schema.Tournament(tour_id=t[0].t_id, name=t[0].t_name, description=t[0].t_desc, date=str(t[0].t_date), last_reg_date=str(t[0].last_reg_date), coach=Schema.Profile(name=t[1].name, usn=t[1].usn, email=t[1].email, dob=str(t[1].dob), role=t[1].role), game=Schema.Add_Game(name=t[2].g_name, type=t[2].g_type))
    return result
def Find_Registration(id:int, db:Session):
    register = db.query(models.User, models.Registration).join(models.Registration.r_player == models.User.usn).filter(models.Registration.r_tour == id).all()
    result = [Schema.Player(name=r[0].name, usn=r[0].usn, email=r[0].email, dob=str(r[0].dob), role=r[0].role) for r in register]
    return result
def Add_Register(id:int, user:str, db:Session):
    try:
        tournament = Find_Tournament(id, db)
        if tournament.last_reg_date >= str(datetime.now().date()):
            new_register = models.Registration(r_tour=id, r_player=user, r_date=str(datetime.now().date()))
            db.add(new_register)
            db.commit()
            db.refresh(new_register)
            return new_register
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Couldn't register due to {e}")