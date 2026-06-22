from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId

from db.server import Store
from auth import CurrentUserType
from models.stores import CreateStore, PatchStore

router = APIRouter(prefix="/api/stores")

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
async def get_all_stores(current_user: CurrentUserType):
    stores = await Store.find_many(
        Store.user_id == current_user.id
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
    
    

    await store.delete()




@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_stores(current_user: CurrentUserType):
    await Store.find_many(
        Store.user_id == current_user.id
    ).delete_many()
