from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from models.users import BaseUser
from db.documents import User
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
import random

secret_key = "111111111111111111111111111111111111111111111111111111111111111111111111"
algorithm = "HS256"
expire_minutes = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

password_hash = PasswordHash.recommended()

type oauth_token = Annotated[str, Depends(oauth2_scheme)]

class InvalidCredentials (HTTPException):
    """
    Raises the following text: "Could not validate credentials"
    """
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials"
        self.headers = { "WWW-Authenticate": "Bearer" }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password (plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def hash_password(plain_password: str):
    return password_hash.hash(plain_password)

async def authenticate(username: str, password: str):
    user = await User.find_one(User.username == username)

    if not user:
        verify_password(password, password_hash.hash(random.randbytes(16).decode("utf-8")))
        return False
    
    return verify_password(password, user.password_hash)

def create_access_token(username:str, expires_delta: timedelta | None = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=expire_minutes)

    data = {
        "sub": username,
        "exp": datetime.now() + expires_delta
    }

    encoded_jwt = jwt.encode(payload=data, key=secret_key, algorithm=algorithm)

    return Token(access_token=encoded_jwt)

def decode_access_token (token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str | None = payload.get("sub")
        return username
    except InvalidTokenError:
        return None

async def get_current_user (token: oauth_token):
    username = decode_access_token(token)

    if not username:
        raise InvalidCredentials()
    
    user = await User.find_one(User.username == username, User.logged_in == True)

    if not user:
        raise InvalidCredentials()
    
    return user

type current_user_type = Annotated[User, Depends(get_current_user)]
