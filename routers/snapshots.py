from typing import Any, Callable, Annotated

from fastapi import APIRouter, HTTPException, Query, status
from beanie import Document, PydanticObjectId
from beanie.operators import In
from pydantic import BaseModel

from auth import CurrentUserType
from db.documents import Store, User
from db.server import Snapshot, Product
from models.snapshots import CreateSnapshot, PatchSnapshot, SearchSnapshot
from routers.products import Product
from routers.stores import get_all_stores

router = APIRouter(prefix="/api/snapshot")

type SearchTerms = Annotated[SearchSnapshot, Query()]

async def verify_snapshot(snapshot: Snapshot | None, user: User):
    if not snapshot: return False

    store = await Store.find_one(
        Store.id == snapshot.store_id,
        Store.user_id == user.id
    )

    product = await Product.find_one(
        Product.id == snapshot.product_id,
        Product.user_id == user.id
    )

    if not store: return False
    if not product: return False

    return True

@router.get(
    "/get/{snapshot_id}",
    response_model=Snapshot|None
)
async def get_snapshot_by_id(snapshot_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(snapshot_id)

    snapshot = await Snapshot.find_one(
        Snapshot.id == object_id
    )

    verified = await verify_snapshot(snapshot, current_user)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snapshot could not be found."
        )

    return snapshot


@router.get(
    "/all/get",
    response_model=list[Snapshot]
)
async def get_all_snapshots(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchSnapshot()
):
    stores = await get_all_stores(current_user=current_user)
    store_ids = [ store.id for store in stores if store.id ]

    snapshots: list[Snapshot] = []

    if len(store_ids) == 0: return snapshots

    snapshots.extend(await Snapshot.find(
        In(Snapshot.store_id, store_ids),
        search_terms.model_dump(exclude_none=True)
    ).to_list())

    return snapshots


@router.get(
    "/product/{product_id}",
    response_model=list[Snapshot]
)
async def get_snapshots_by_product_id(product_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(product_id)

    product = await Product.find_one(Product.id == current_user.id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    snapshots = await Snapshot.find_many(
        Snapshot.product_id == object_id
    ).to_list()

    return snapshots


@router.post(
    "/create",
    response_model=Snapshot
)
async def create_new_snapshot(snapshot_data: CreateSnapshot, current_user: CurrentUserType):
    product = await Product.find_one(Product.id == current_user.id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create snapshot: product not found."
        )

    if not current_user.id: return None

    snapshot = Snapshot(
        product_id=snapshot_data.product_id,
        store_id=snapshot_data.store_id,
        production_cost=snapshot_data.production_cost,
        selling_cost=snapshot_data.selling_cost,
        currency=snapshot_data.currency
    )

    verified = await verify_snapshot(snapshot, current_user)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Store does not belong to user."
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
        Snapshot.id == object_id
    )

    store = await verify_snapshot(snapshot, current_user)

    if not snapshot or not store:
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
        Snapshot.id == object_id
    )

    verified = await verify_snapshot(snapshot, current_user)

    if not snapshot or not verified:
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

    product = await Product.find_one(
        Product.id == object_id,
        Product.user_id == current_user.id
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    await Snapshot.find_many(
        Snapshot.product_id == object_id
    ).delete_many()

@router.delete(
    "/all/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_snapshots(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchSnapshot()
):
    stores = await get_all_stores(current_user=current_user)
    store_ids = [ store.id for store in stores if store.id ]

    if not store_ids: return

    await Snapshot.find_many(
        In(Snapshot.store_id, store_ids),
        search_terms.model_dump(exclude_none=True)
    ).delete_many()
