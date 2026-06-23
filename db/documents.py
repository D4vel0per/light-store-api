from beanie import Document, PydanticObjectId

from models import billing, products, selling, snapshots, stores, transactions, users
from models.general import BaseDB


class User(Document, users.BaseUser, BaseDB):
    password_hash: str
    logged_in: bool
    class Settings:
        name = "users"

class Store(Document, stores.CreateStore, BaseDB):
    user_id: PydanticObjectId
    class Settings:
        name = "stores"

class Transaction(Document, transactions.CreateTransaction, BaseDB):
    user_id: PydanticObjectId
    class Settings:
        name = "transactions"

class Snapshot(Document, snapshots.CreateSnapshot, BaseDB):
    class Settings:
        name = "snapshots"

class Product(Document, products.CreateProduct, BaseDB):
    user_id: PydanticObjectId
    class Settings:
        name = "products"

class Billing(Document, billing.CreateBilling, BaseDB):
    class Settings:
        name = "billings"

class Selling(Document, selling.CreateSelling, BaseDB):
    class Settings:
        name = "sellings"







