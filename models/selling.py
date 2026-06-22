from beanie import PydanticObjectId

from models.general import BaseDB, ProductDescriptor
from models.stores import CURRENCIES

class BaseSelling(BaseDB):
    transaction_id: PydanticObjectId

class CreateSelling(BaseSelling):
    total: int
    description: str
    product: ProductDescriptor
    currency: CURRENCIES

class PatchSelling(BaseSelling):
    total: int | None = None
    description: str | None = None
    product: ProductDescriptor | None = None
    currency: CURRENCIES | None = None