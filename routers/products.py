from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/products")


@router.get(
    "/{product_id}"
)
async def get_product_by_name(product_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_products(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_product(product_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{product_id}"
)
async def update_product(product_id: str, product_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{product_id}"
)
async def delete_product(product_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_products(token: str):
    pass
