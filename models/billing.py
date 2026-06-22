from beanie import PydanticObjectId

from models.general import BaseDB, ProductDescriptor
from models.stores import CURRENCIES

class BaseBilling(BaseDB):
    transaction_id: PydanticObjectId

class CreateBilling(BaseBilling):
    total: int
    description: str
    product: ProductDescriptor | None = None
    currency: CURRENCIES

class PatchBilling(BaseBilling):
    total: int | None = None
    description: str | None = None
    product: ProductDescriptor | None = None
    currency: CURRENCIES | None = None