from fastapi import APIRouter

from fastapi.security import OAuth2PasswordRequestForm

from db.server import User, Transaction
from auth import (
    Token,
    current_user_type, 
    InvalidCredentials, 
    create_access_token, 
    authenticate,
    hash_password
)
from models.users import BaseUser, PatchUser

router = APIRouter(prefix="/api/users")

@router.get(
    "/me",
    response_model=BaseUser
)
async def get_own_details(current_user: current_user_type):
    return BaseUser(**current_user.model_dump())

@router.get(
    "/public/{username}",
    response_model=BaseUser|None
)
async def fetch_user_details(username, _: current_user_type):
    user = await User.find_one(User.username == username)

    return BaseUser(**user.model_dump()) if user else None

@router.post(
    "/login",
    response_model=Token
)
async def login(form_data: OAuth2PasswordRequestForm):
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
async def signin(form_data: OAuth2PasswordRequestForm):
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

    return await new_user.insert()

@router.post(
    "/logout"
)
async def logout(current_user: current_user_type):
    await current_user.set({
        User.logged_in: False
    })

@router.post(
    "/update-account"
)
async def update_account(account_data: PatchUser, current_user: current_user_type):
    await current_user.set(account_data.model_dump(exclude_none=True, exclude_unset=True))

@router.delete(
    "/delete-account"
)
async def delete_account(current_user: current_user_type):
    await current_user.delete()
    # Call other deletion methods here
