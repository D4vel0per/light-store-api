from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/transactions")


@router.get(
    "/{transaction_id}"
)
async def get_transaction_by_name(transaction_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_transactions(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_transaction(transaction_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{transaction_id}"
)
async def update_transaction(transaction_id: str, transaction_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{transaction_id}"
)
async def delete_transaction(transaction_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_transactions(token: str):
    pass
