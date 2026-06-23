from beanie import PydanticObjectId
from pydantic import BaseModel

from models.general import ProductDescriptor
from models.stores import CURRENCIES

class BaseSelling(BaseModel):
    transaction_id: PydanticObjectId

class SearchSelling(BaseModel):
    transaction_id: str | None = None
    total: int | None = None
    description: str | None = None
    currency: CURRENCIES | None = None

class CreateSelling(BaseSelling):
    total: int
    description: str
    product: ProductDescriptor
    currency: CURRENCIES

class PatchSelling(BaseModel):
    total: int | None = None
    description: str | None = None
    product: ProductDescriptor | None = None
    currency: CURRENCIES | None = None