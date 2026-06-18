from beanie import PydanticObjectId
from pydantic import BaseModel

from models.general import BaseDB

class BaseBilling(BaseDB):
    transaction_id: PydanticObjectId

class ProductDescriptor (BaseModel):
    quantity: int
    price_per_unit: int
    product_id: PydanticObjectId

class CreateBilling(BaseBilling):
    total: int
    description: str
    product: ProductDescriptor | None = None

class PatchBilling(BaseBilling):
    total: int | None = None
    description: str | None = None
    product: ProductDescriptor | None = None