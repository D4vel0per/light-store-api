from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/snapshot")

@router.get(
    "/{snapshot_id}"
)
async def get_snapshot_by_name(snapshot_id: str, token: str):
    pass


@router.get(
    "/all"
)
async def get_all_snapshots(token: str):
    pass


@router.post(
    "/create"
)
async def create_new_snapshot(snapshot_data: dict[str, Any], token: str):
    pass

@router.post(
    "/update/{snapshot_id}"
)
async def update_snapshot(snapshot_id: str, snapshot_data: dict[str, Any], token: str):
    pass

@router.delete(
    "/delete/{snapshot_id}"
)
async def delete_snapshot_item(item_id: str, token: str):
    pass

@router.delete(
    "/delete/all"
)
async def delete_all_snapshots(token: str):
    pass
