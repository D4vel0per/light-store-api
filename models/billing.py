from beanie import PydanticObjectId
from pydantic import BaseModel

from models.general import BaseDB, ProductDescriptor
from models.stores import CURRENCIES

class BaseBilling(BaseModel):
    transaction_id: PydanticObjectId

class CreateBilling(BaseBilling):
    total: int
    description: str
    product: ProductDescriptor | None = None
    currency: CURRENCIES

class PatchBilling(BaseModel):
    total: int | None = None
    description: str | None = None
    product: ProductDescriptor | None = None
    currency: CURRENCIES | None = None

class SearchBilling(BaseModel):
    total: int | None = None
    description: str | None = None
    product_id: str | None = None
    currency: CURRENCIES | None = None