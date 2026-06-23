from enum import Enum
from typing import Annotated

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

class CreateStore (BaseModel):
    name: str
    tax_doc: str
    phone_number: E164NumberType
    address: Address

class PatchStore (BaseModel):
    name: str | None = None
    tax_doc: str | None = None
    phone_number: E164NumberType | None = None
    address: Address | None = None

class SearchStore(BaseModel):
    name: str | None = None
    tax_doc: str | None = None
    phone_number: str | None = None