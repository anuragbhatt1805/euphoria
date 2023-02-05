from fastapi import HTTPException, status, Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import Schema
from Database import models
from jose import jwt
from operator import or_
from typing import Optional, Dict

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return authorization

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEY = "25b2e8d86893b06c86bc5a66bfb93ef1ff0de475bb49c7e38280b4d18dd1625a"
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")
ALGORITHM = "HS256"

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass:str, hash_pass:str):
    return pwd_context.verify(plain_pass, hash_pass)


def FindUser(data:Schema.Create_Acc, db:Session):
    users = db.query(models.User).filter(or_(data.usn.lower() == models.User.usn, data.email == models.User.email)).first()
    if not users:
        return users
    else:
        return True

def AddUser(data:Schema.Create_Acc, db:Session):
    try:
        new_user = models.User(name=data.name, usn=data.usn.lower(), email=data.email, dob=data.dob, password=hash_pass(data.password), role=data.role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User Account was not created due to following issue: {e}")

def create_access_token(data:dict, user:str):
    to_encode = data.copy()
    to_encode.update({'user':user})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_token

def get_user(username:str, db:Session):
    if len(username) <= 10:
        user = db.query(models.User).filter(models.User.usn == username.lower()).first()
    else:
        user = db.query(models.User).filter(models.User.email == username).first()
    return user

def Login(data:OAuth2PasswordRequestForm, db:Session):
    user = get_user(data.username, db)
    if not user:
        return None
    else:
        if verify_password(data.password, user.password):
            access_token = create_access_token({"username":user.usn, "password":data.password}, user.role)
            return Schema.Token(access_token=access_token, token_type='bearer', user=user.role)
        else:
            return None

def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials Please login to avail services /login",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try :
        result = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username : str = result.get("username")
        role : str = result.get("user")
        if username is None:
            return None
        data = Schema.UserData(username = username, user = role)
    except Exception as e:
        raise credentials_exception
    return data