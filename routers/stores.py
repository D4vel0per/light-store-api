from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import In
from fastapi import APIRouter, HTTPException, Query, status

from db.documents import Billing, Snapshot, Transaction
from db.server import Store
from db.server import Selling
from auth import CurrentUserType
from models.stores import CreateStore, PatchStore, SearchStore
from routers.transactions import delete_transactions_by_store_id

router = APIRouter(prefix="/api/stores")

type SearchTerms = Annotated[SearchStore, Query()]

@router.get(
    "/get/{store_id}",
    response_model=Store|None
)
async def get_store_by_id(store_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(store_id)

    store = await Store.find_one(
        Store.id == object_id,
        Store.user_id == current_user.id
    )

    return store


@router.get(
    "/all",
    response_model=list[Store]
)
async def get_all_stores(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchStore()
):
    stores = await Store.find_many(
        Store.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ).to_list()

    return stores


@router.post(
    "/create",
    response_model=Store
)
async def create_new_store(store_data: CreateStore, current_user: CurrentUserType):
    if not current_user.id: return None
    
    store = Store(
        name=store_data.name,
        tax_doc=store_data.tax_doc,
        phone_number=store_data.phone_number,
        address=store_data.address,
        user_id=current_user.id
    )

    return await store.insert()


@router.post(
    "/update/{store_id}",
    response_model=Store
)
async def update_store(
    store_id: str,
    store_data: PatchStore,
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(store_id)

    store = await Store.find_one(
        Store.id == object_id,
        Store.user_id == current_user.id
    )

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update store: store could not be found."
        )

    return await store.set(
        store_data.model_dump(exclude_unset=True)
    )


@router.delete(
    "/delete/{store_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_store(store_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(store_id)

    store = await Store.find_one(
        Store.id == object_id,
        Store.user_id == current_user.id
    )

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete store: store could not be found."
        )
    
    if not store.id: return
    
    await delete_transactions_by_store_id(
        store_id=store.id.binary.decode("utf-8"),
        current_user=current_user
    )
    await Snapshot.find_many(Snapshot.store_id == store.id).delete_many()

    await store.delete()

@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_stores(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchStore()
):
    stores = await Store.find_many(
        Store.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ).to_list()

    store_ids = [store.id for store in stores if store.id]

    if not store_ids:
        return

    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id,
        In(Transaction.store_id, store_ids)
    ).to_list()

    transaction_ids = [t.id for t in transactions if t.id]

    if transaction_ids:
        await Billing.find_many(
            In(Billing.transaction_id, transaction_ids)
        ).delete_many()
        await Transaction.find_many(
            In(Transaction.id, transaction_ids)
        ).delete_many()

    await Selling.find_many(
        In(Selling.transaction_id, transaction_ids)
    ).delete_many()

    await Snapshot.find_many(
        In(Snapshot.store_id, store_ids)
    ).delete_many()

    await Store.find_many(
        In(Store.id, store_ids)
    ).delete_many()
