from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/selling")


@router.get(
    "/{selling_id}"
)
async def get_selling_by_name(selling_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_sellings(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_selling(selling_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{selling_id}"
)
async def update_selling(selling_id: str, selling_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{selling_id}"
)
async def delete_selling(selling_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_sellings(token: str):
    pass
