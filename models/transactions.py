from beanie import PydanticObjectId

from models.general import BaseDB

class BaseTransaction (BaseDB):
    store_id: PydanticObjectId
    user_id: PydanticObjectId

class CreateTransaction (BaseTransaction):
    balance: int
    description: str

class PatchTransaction (BaseTransaction):
    balance: int | None = None
    description: str | None = None
