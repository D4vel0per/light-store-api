from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId

from auth import CurrentUserType
from db.server import Snapshot, Product
from models.snapshots import CreateSnapshot, PatchSnapshot
from routers.products import get_product_by_id

router = APIRouter(prefix="/api/snapshot")

@router.get(
    "/get/{snapshot_id}",
    response_model=Snapshot|None
)
async def get_snapshot_by_id(snapshot_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(snapshot_id)

    snapshot = await Snapshot.find_one(
        Snapshot.id == object_id,
        Snapshot.user_id == current_user.id
    )

    return snapshot


@router.get(
    "/all",
    response_model=list[Snapshot]
)
async def get_all_snapshots(current_user: CurrentUserType):
    snapshots = await Snapshot.find_many(
        Snapshot.user_id == current_user.id
    ).to_list()

    return snapshots


@router.get(
    "/product/{product_id}",
    response_model=list[Snapshot]
)
async def get_snapshots_by_product_id(product_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(product_id)

    product = await get_product_by_id(product_id, current_user)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    snapshots = await Snapshot.find_many(
        Snapshot.product_id == object_id,
        Snapshot.user_id == current_user.id
    ).to_list()

    return snapshots


@router.post(
    "/create",
    response_model=Snapshot
)
async def create_new_snapshot(snapshot_data: CreateSnapshot, current_user: CurrentUserType):
    product = await get_product_by_id(
        snapshot_data.product_id.binary.decode("utf-8"),
        current_user
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create snapshot: product not found."
        )

    if not current_user.id: return None

    snapshot = Snapshot(
        product_id=snapshot_data.product_id,
        user_id=current_user.id,
        production_cost=snapshot_data.production_cost,
        selling_cost=snapshot_data.selling_cost,
        currency=snapshot_data.currency
    )

    return await snapshot.insert()


@router.post(
    "/update/{snapshot_id}",
    response_model=Snapshot
)
async def update_snapshot(
    snapshot_id: str,
    snapshot_data: PatchSnapshot,
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(snapshot_id)

    snapshot = await Snapshot.find_one(
        Snapshot.id == object_id,
        Snapshot.user_id == current_user.id
    )

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update snapshot: snapshot could not be found."
        )

    return await snapshot.set(
        snapshot_data.model_dump(exclude_unset=True)
    )


@router.delete(
    "/delete/{snapshot_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_snapshot(snapshot_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(snapshot_id)

    snapshot = await Snapshot.find_one(
        Snapshot.id == object_id,
        Snapshot.user_id == current_user.id
    )

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete snapshot: snapshot could not be found."
        )

    await snapshot.delete()


@router.delete(
    "/delete/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_snapshots_by_product_id(product_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(product_id)

    product = await Product.find_one(Product.id == object_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    await Snapshot.find_many(
        Snapshot.product_id == object_id,
        Snapshot.user_id == current_user.id
    ).delete_many()


@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_snapshots(current_user: CurrentUserType):
    await Snapshot.find_many(
        Snapshot.user_id == current_user.id
    ).delete_many()
