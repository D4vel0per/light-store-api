from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/stores")

@router.get(
    "/{store_id}"
)
async def get_store_by_name(store_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_stores(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_store(store_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{store_id}"
)
async def update_store(store_id: str, store_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{store_id}"
)
async def delete_store(store_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_stores(token: str):
    pass
