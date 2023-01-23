from sqlalchemy.orm import Session
from . import Schema
from Database import models

def Display_Profile(username:str, db:Session):
    profile = db.query(models.User).filter(models.User.usn == username).first()
    result = Schema.Profile(name=profile.name, usn=profile.usn, email=profile.email, dob=str(profile.dob), role=profile.role)
    return result
    