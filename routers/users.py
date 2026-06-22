from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from db.server import User
from auth import (
    Token,
    CurrentUserType, 
    InvalidCredentials, 
    create_access_token, 
    authenticate,
    hash_password
)
from models.users import BaseUser, PatchUser
from routers.billing import delete_all_billings
from routers.stores import delete_all_stores
from routers.transactions import delete_all_transactions

router = APIRouter(prefix="/api/users")

@router.get(
    "/me",
    response_model=BaseUser
)
async def get_own_details(current_user: CurrentUserType):
    return BaseUser(**current_user.model_dump())

@router.get(
    "/public/{username}",
    response_model=BaseUser|None
)
async def fetch_user_details(username, _: CurrentUserType):
    user = await User.find_one(User.username == username)

    return BaseUser(**user.model_dump()) if user else None

@router.post(
    "/login",
    response_model=Token
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    password = form_data.password
    username = form_data.username

    authenticated = await authenticate(username=username, password=password)

    if not authenticated:
        raise InvalidCredentials()
    
    await User.find_one(User.username == username).set({
        User.logged_in: True
    })
    
    return create_access_token(username=username)

@router.post(
    "/signin"
)
async def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    password = form_data.password
    # The username and email will be separated like "user - email@gmail.com"
    user_info = form_data.username.split(" - ") 
    email = user_info.pop()
    username = " - ".join(user_info)

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        logged_in=True
    )

    await new_user.insert()

    return BaseUser(**new_user.model_dump())

@router.post(
    "/logout"
)
async def logout(current_user: CurrentUserType):
    await current_user.set({
        User.logged_in: False
    })

@router.post(
    "/update-account"
)
async def update_account(account_data: PatchUser, current_user: CurrentUserType):
    await current_user.set(account_data.model_dump(exclude_unset=True))

@router.delete(
    "/delete-account"
)
async def delete_account(current_user: CurrentUserType):
    await delete_all_billings(current_user=current_user)
    await delete_all_transactions(current_user=current_user)
    await delete_all_stores(current_user=current_user)
    await current_user.delete()
