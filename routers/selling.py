from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId

from db.server import Selling, Transaction
from auth import CurrentUserType
from models.selling import CreateSelling, PatchSelling

router = APIRouter(prefix="/api/selling")


@router.get(
    "/get/{selling_id}",
    response_model=Selling|None
)
async def get_selling_by_id(selling_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(selling_id)

    selling = await Selling.find_one(
        Selling.id == object_id
    )

    if selling:
        transaction = await Transaction.find_one(
            Transaction.id == selling.transaction_id,
            Transaction.user_id == current_user.id
        )
        if not transaction:
            return None

    return selling


@router.get(
    "/all",
    response_model=list[Selling]
)
async def get_all_sellings(current_user: CurrentUserType):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id
    ).to_list()

    transaction_ids = [t.id for t in transactions]

    sellings = []

    for t_id in transaction_ids:

        sellings.extend(await Selling.find_many(
            Selling.transaction_id == t_id
        ).to_list())

    return sellings


@router.get(
    "/transaction/{transaction_id}",
    response_model=list[Selling]
)
async def get_sellings_by_transaction_id(transaction_id: str, current_user: CurrentUserType):
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

    sellings = await Selling.find_many(
        Selling.transaction_id == object_id
    ).to_list()

    return sellings


@router.post(
    "/create",
    response_model=Selling
)
async def create_new_selling(selling_data: CreateSelling, current_user: CurrentUserType):
    transaction = await Transaction.find_one(
        Transaction.id == selling_data.transaction_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot create selling: transaction not found or does not belong to user."
        )

    selling = Selling(
        transaction_id=selling_data.transaction_id,
        total=selling_data.total,
        description=selling_data.description,
        product=selling_data.product,
        currency=selling_data.currency
    )

    return await selling.insert()


@router.post(
    "/update/{selling_id}",
    response_model=Selling
)
async def update_selling(
    selling_id: str,
    selling_data: PatchSelling,
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(selling_id)

    selling = await Selling.find_one(
        Selling.id == object_id
    )

    if not selling:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update selling: selling could not be found."
        )

    transaction = await Transaction.find_one(
        Transaction.id == selling.transaction_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update selling: selling does not belong to user."
        )

    return await selling.set(
        selling_data.model_dump(exclude_unset=True)
    )


@router.delete(
    "/delete/{selling_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_selling(selling_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(selling_id)

    selling = await Selling.find_one(
        Selling.id == object_id
    )

    if not selling:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete selling: selling could not be found."
        )

    transaction = await Transaction.find_one(
        Transaction.id == selling.transaction_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete selling: selling does not belong to user."
        )

    await selling.delete()


@router.delete(
    "/delete/transaction/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_sellings_by_transaction(transaction_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(transaction_id)

    transaction = await Transaction.find_one(
        Transaction.id == object_id,
        Transaction.user_id == current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete sellings: transaction not found or does not belong to user."
        )

    await Selling.find_many(
        Selling.transaction_id == object_id
    ).delete_many()


@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_sellings(current_user: CurrentUserType):
    transactions = await Transaction.find_many(
        Transaction.user_id == current_user.id
    ).to_list()

    for transaction in transactions:
        if not transaction.id: continue
        await delete_sellings_by_transaction(
            transaction.id.binary.decode("utf-8"),
            current_user
        )
