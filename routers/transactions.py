from typing import Annotated

from beanie.operators import In
from fastapi import APIRouter, Depends, HTTPException, Query, status
from beanie import PydanticObjectId

from db.documents import Billing, Selling, Store
from db.server import Transaction
from auth import CurrentUserType
from models.transactions import CreateTransaction, PatchTransaction, SearchTransaction
from routers.billing import delete_all_billings
from routers.selling import delete_all_sellings

router = APIRouter(prefix="/api/transactions")

type SearchTerms = Annotated[SearchTransaction, Query()]

@router.get(
    "/get/{transaction_id}",
    response_model=Transaction|None
)
async def get_transaction_by_id(transaction_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(transaction_id)

    transaction = await Transaction.find_one(
        Transaction.id == object_id,
        Transaction.user_id == current_user.id
    )

    return transaction

@router.get(
    "/all",
    response_model=list[Transaction]
)
async def get_all_transactions(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchTransaction()
):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ).to_list()

    return transactions

@router.post(
    "/create",
    response_model=Transaction
)
async def create_new_transaction(transaction_data: CreateTransaction, current_user: CurrentUserType):
    if not current_user.id: return None

    store = await Store.find_one(
        Store.id == transaction_data.store_id,
        Store.user_id == current_user.id
    )

    if not store:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create transaction: transaction does not belong to store"
        )

    transaction = Transaction(
        store_id=transaction_data.store_id,
        user_id=current_user.id,
        balance=transaction_data.balance,
        description=transaction_data.description,
        currency=transaction_data.currency
    )

    return await transaction.insert()

@router.post(
    "/update/{transaction_id}",
    response_model=Transaction
)
async def update_transaction(
    transaction_id: str, 
    transaction_data: PatchTransaction, 
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(transaction_id)

    transaction = await Transaction.find_one(
        Transaction.id == object_id,
        Transaction.user_id == current_user.id
    )

    if not transaction: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update transaction: transaction could not be found."
        )

    return await transaction.set(
        transaction_data.model_dump(exclude_unset=True)
    )

@router.get(
    "/store/{store_id}",
    response_model=list[Transaction]
)
async def get_transactions_by_store_id(store_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(store_id)

    store = await Store.find_one(
        Store.id == object_id,
        Store.user_id == current_user.id
    )

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found or does not belong to user."
        )

    transactions = await Transaction.find_many(
        Transaction.store_id == object_id,
        Transaction.user_id == current_user.id
    ).to_list()

    return transactions

@router.delete(
    "/delete/store/{store_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_transactions_by_store_id(store_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(store_id)

    store = await Store.find_one(
        Store.id == object_id,
        Store.user_id == current_user.id
    )

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete transactions: store not found or does not belong to user."
        )
    
    transactions = Transaction.find_many(
        Transaction.store_id == object_id,
        Transaction.user_id == current_user.id
    )

    t_ids = [ t.id for t in (await transactions.to_list()) if t.id]
    
    await Billing.find_many(
        In(
            Billing.transaction_id, 
            t_ids
        )
    ).delete_many()

    await Selling.find_many(
        In(
            Selling.transaction_id, 
            t_ids
        )
    ).delete_many()

    await transactions.delete_many()

@router.delete(
    "/delete/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_transaction(transaction_id: str, current_user: CurrentUserType):
    transaction = await get_transaction_by_id(
        transaction_id=transaction_id, current_user=current_user
    )
    if not transaction: return None

    await Selling.find_many(Selling.transaction_id == transaction.id).delete_many()
    await Billing.find_many(Selling.transaction_id == transaction.id).delete_many()

    await transaction.delete()

@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_transactions(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchTransaction()
):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ).to_list()

    ids = [t.id for t in transactions if t.id]

    if not ids:
        return

    await Billing.find_many(
        In(Billing.transaction_id, ids)
    ).delete_many()

    await Selling.find_many(
        In(Selling.transaction_id, ids)
    ).delete_many()

    await Transaction.find_many(
        In(Transaction.id, ids)
    ).delete_many()
