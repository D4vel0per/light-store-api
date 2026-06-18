from beanie import PydanticObjectId

from models.general import BaseDB

class BaseSelling(BaseDB):
    product_id: PydanticObjectId
    transaction_id: PydanticObjectId

class CreateSelling(BaseSelling):
    quantity: int
    total: int

class PatchSelling(BaseSelling):
    quantity: int | None = None
    total: int | None = None