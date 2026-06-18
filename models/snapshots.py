from beanie import PydanticObjectId

from models.general import BaseDB
from models.stores import CURRENCIES

class BaseSnapshot(BaseDB):
    product_id: PydanticObjectId
    user_id: PydanticObjectId

class CreateSnapshot(BaseSnapshot):
    production_cost: int
    selling_cost: int
    currency: CURRENCIES

class PatchSnapshot(BaseSnapshot):
    production_cost: int | None = None
    selling_cost: int | None = None
    currency: CURRENCIES | None = None