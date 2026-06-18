from enum import Enum
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
import phonenumbers

E164NumberType = Annotated[str | phonenumbers.PhoneNumber, PhoneNumberValidator(number_format='E164')]

class Address (BaseModel):
    region: str
    city: str
    country_code: str

class CURRENCIES (str, Enum):
    USD = "USD"
    VES = "VES"

class BaseStore(BaseModel):
    user_id: PydanticObjectId

class CreateStore (BaseStore):
    name: str
    tax_doc: str
    phone_number: E164NumberType
    internal_currency: CURRENCIES
    product_currency: CURRENCIES
    address: Address

class PatchStore (BaseStore):
    name: str | None = None
    tax_doc: str | None = None
    phone_number: E164NumberType | None = None
    internal_currency: CURRENCIES | None = None 
    product_currency: CURRENCIES | None = None 
    address: Address | None = None