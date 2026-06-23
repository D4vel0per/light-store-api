from beanie import PydanticObjectId
from pydantic import BaseModel

from models.stores import CURRENCIES

class BaseTransaction (BaseModel):
    store_id: PydanticObjectId
    user_id: PydanticObjectId

class SearchTransaction(BaseModel):
    store_id: str | None = None
    balance: int | None = None
    description: str | None = None
    currency: CURRENCIES | None = None

class CreateTransaction (BaseTransaction):
    balance: int
    description: str
    currency: CURRENCIES

class PatchTransaction (BaseModel):
    balance: int | None = None
    description: str | None = None
    currency: CURRENCIES | None = None
