from beanie import PydanticObjectId

from models.general import BaseDB
from models.stores import CURRENCIES

class BaseTransaction (BaseDB):
    store_id: PydanticObjectId
    user_id: PydanticObjectId

class CreateTransaction (BaseTransaction):
    balance: int
    description: str
    currency: CURRENCIES

class PatchTransaction (BaseTransaction):
    balance: int | None = None
    description: str | None = None
    currency: CURRENCIES | None = None
