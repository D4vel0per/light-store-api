from beanie import PydanticObjectId
from pydantic import BaseModel

from models.stores import CURRENCIES

class BaseSnapshot(BaseModel):
    product_id: PydanticObjectId
    store_id: PydanticObjectId

class SearchSnapshot(BaseModel):
    product_id: str | None = None
    store_id: str | None = None
    production_cost: int | None = None
    selling_cost: int | None = None
    currency: CURRENCIES | None = None

class CreateSnapshot(BaseSnapshot):
    production_cost: int
    selling_cost: int
    currency: CURRENCIES

class PatchSnapshot(BaseModel):
    production_cost: int | None = None
    selling_cost: int | None = None
    currency: CURRENCIES | None = None