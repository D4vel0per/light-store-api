from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/users")

@router.get(
    "/me"
)
async def get_own_details(token: str):
    pass

@router.get(
    "/public"
)
async def get_public_user_details(token: str):
    pass

@router.post(
    "/login"
)
async def login(token: str):
    pass


@router.post(
    "/signin"
)
async def signin(transaction_data: dict[str, Any], token: str):
    pass

@router.post(
    "/logout"
)
async def logout(token: str):
    pass

@router.post(
    "/update-account"
)
async def update_account(account_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete-account"
)
async def delete_account(token: str):
    pass
