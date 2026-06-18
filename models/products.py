from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from models.general import BaseDB

class BaseProduct(BaseDB):
    store_id: PydanticObjectId
    snapshot_id: PydanticObjectId

class LifeCicle(BaseModel):
    production: datetime
    expiration: datetime

class Measurement:
    def __init__(self, singular: str, plural: str):
        self.singular = singular
        self.plural = plural

    def measurement(self, quantity: int):
        return self.singular if quantity == 1 else self.plural

class CreateProduct(BaseProduct):
    name: str
    brand: str
    description: str | None = None
    descriptors: dict[str, str] = Field(default_factory=lambda: {})
    code: str
    life_cicle: LifeCicle | None = None
    quantity: int
    measurement: Measurement | None = None
    tags: list[str] = Field(default_factory=lambda: [])

class PatchProduct(BaseProduct):
    name: str | None = None
    brand: str | None = None
    description: str | None = None
    descriptors: dict[str, str] | None = None
    code: str | None = None
    life_cicle: LifeCicle | None = None
    quantity: int | None = None
    measurement: Measurement | None = None
    tags: list[str] | None = None