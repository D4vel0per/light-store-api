from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId

from db.server import Billing, Transaction
from auth import CurrentUserType
from models.billing import CreateBilling, PatchBilling

router = APIRouter(prefix="/api/billing")

@router.get(
    "/get/{billing_id}",
    response_model=Billing|None
)
async def get_billing_by_id(billing_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(billing_id)

    billing = await Billing.find_one(Billing.id == object_id)
    
    if billing:
        transaction = await Transaction.find_one(
            Transaction.id == billing.transaction_id,
            Transaction.user_id == current_user.id
        )
        if not transaction:
            return None
    
    return billing


@router.get(
    "/all",
    response_model=list[Billing]
)
async def get_all_billings(current_user: CurrentUserType):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id
    ).to_list()
    
    transaction_ids = [t.id for t in transactions]

    billings = []

    for t_id in transaction_ids:
        billings.extend(await Billing.find_many(
            Billing.transaction_id == t_id
        ).to_list())
    
    return billings


@router.get(
    "/transaction/{transaction_id}",
    response_model=list[Billing]
)
async def get_billings_by_transaction_id(transaction_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(transaction_id)

    transaction = await Transaction.find_one(
        Transaction.id == object_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found or does not belong to user."
        )

    billings = await Billing.find_many(
        Billing.transaction_id == object_id
    ).to_list()

    return billings


@router.post(
    "/create",
    response_model=Billing
)
async def create_new_billing(billing_data: CreateBilling, current_user: CurrentUserType):
    transaction = await Transaction.find_one(
        Transaction.id == billing_data.transaction_id,
        Transaction.user_id == current_user.id
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create billing: transaction not found or does not belong to user."
        )

    billing = Billing(
        transaction_id=billing_data.transaction_id,
        total=billing_data.total,
        description=billing_data.description,
        product=billing_data.product,
        currency=transaction.currency
    )

    return await billing.insert()

@router.post(
    "/update/{billing_id}",
    response_model=Billing
)
async def update_billing(
    billing_id: str, 
    billing_data: PatchBilling, 
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(billing_id)

    billing = await Billing.find_one(Billing.id == object_id)

    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update billing: billing could not be found."
        )
    
    transaction = await Transaction.find_one(
        Transaction.id == billing.transaction_id,
        Transaction.user_id == current_user.id
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update billing: billing does not belong to user."
        )

    return await billing.set(
        billing_data.model_dump(exclude_unset=True)
    )

@router.delete(
    "/delete/{billing_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_billing(billing_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(billing_id)
    
    billing = await Billing.find_one(Billing.id == object_id)
    
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete billing: billing could not be found."
        )
    
    transaction = await Transaction.find_one(
        Transaction.id == billing.transaction_id,
        Transaction.user_id == current_user.id
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete billing: billing does not belong to user."
        )
    
    await billing.delete()

@router.delete(
    "/delete/transaction/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_billings_by_transaction(transaction_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(transaction_id)

    transaction = await Transaction.find_one(
        Transaction.id == object_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete billings: transaction not found or does not belong to user."
        )

    await Billing.find_many(
        Billing.transaction_id == object_id
    ).delete_many()


@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_billings(current_user: CurrentUserType):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id
    ).to_list()

    for transaction in transactions:
        if not transaction.id: continue
        await delete_billings_by_transaction(
            transaction.id.binary.decode("utf-8"),
            current_user
        )
