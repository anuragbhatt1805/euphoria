from pydantic import BaseModel
from typing import List


## <<<--------SignUP-------->>>
class Create_Acc(BaseModel):
    name : str
    usn : str
    email : str
    dob : str
    password : str
    role : str
    class Config():
        orm_mode = True

## <<<--------Login-------->>>
class Token(BaseModel):
    access_token : str
    token_type : str
    user : str
    class Config():
        orm_mode = True

class UserData(BaseModel):
    username : str
    user : str
    class Config():
        orm_mode = True

## <<<--------Admin-------->>>
class Profile(BaseModel):
    name : str
    usn : str
    email : str
    dob : str
    role : str
    class Config():
        orm_mode = True

class Game(BaseModel):
    game_id : int
    game_name : str
    game_type : str
    class Config():
        orm_mode = True

class Add_Game(BaseModel):
    name : str
    type : str
    class Config():
        orm_mode = True

class Tournament(BaseModel):
    tour_id : int
    name : str
    description : str
    date : str
    last_reg_date : str
    coach : Profile
    game : Add_Game
    class Config():
        orm_mode = True

class Add_Tournament(BaseModel):
    name : str
    description : str
    date : str
    last_reg_date : str
    coach : str
    game : int
    class Config():
        orm_mode = True


## <<<--------Tournament-------->>>
class Registration(BaseModel):
    tour : int
    player : str
    date : str
    class Config():
        orm_mode=True