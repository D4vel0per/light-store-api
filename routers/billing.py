from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/billing")

@router.get(
    "/{billing_id}"
)
async def get_billing_by_name(billing_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_billings(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_billing(billing_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{billing_id}"
)
async def update_billing(billing_id: str, billing_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{billing_id}"
)
async def delete_billing(billing_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_billings(token: str):
    pass
