from datetime import datetime

from pydantic import BaseModel, Field

class SearchProduct(BaseModel):
    name: str | None = None
    brand: str | None = None
    description: str | None = None
    code: str | None = None
    tags: list[str] | None = None

class LifeCicle(BaseModel):
    production: datetime
    expiration: datetime

class Measurement(BaseModel):
    singular: str
    plural: str
    def measurement(self, quantity: int):
        return self.singular if quantity == 1 else self.plural

class CreateProduct(BaseModel):
    name: str
    brand: str
    description: str | None = None
    descriptors: dict[str, str] | None = Field(default_factory=lambda: {})
    code: str
    life_cicle: LifeCicle | None = None
    quantity: int
    measurement: Measurement | None = None
    tags: list[str] = Field(default_factory=lambda: [])

class PatchProduct(BaseModel):
    name: str | None = None
    brand: str | None = None
    description: str | None = None
    descriptors: dict[str, str] | None = None
    code: str | None = None
    life_cicle: LifeCicle | None = None
    quantity: int | None = None
    measurement: Measurement | None = None
    tags: list[str] | None = None