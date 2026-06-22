from beanie import Document, Link, PydanticObjectId

from models import billing, products, selling, snapshots, stores, transactions, users

class User(Document, users.BaseUser):
    password_hash: str
    logged_in: bool
    class Settings:
        name = "users"

class Store(Document, stores.CreateStore):
    class Settings:
        name = "stores"

class Transaction(Document, transactions.CreateTransaction):
    class Settings:
        name = "transactions"

class Snapshot(Document, snapshots.CreateSnapshot):
    class Settings:
        name = "snapshots"

class Product(Document, products.CreateProduct):
    class Settings:
        name = "products"

class Billing(Document, billing.CreateBilling):
    class Settings:
        name = "billings"

class Selling(Document, selling.CreateSelling):
    class Settings:
        name = "sellings"







