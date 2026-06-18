from beanie import Document, Link

from models import billing, products, selling, snapshots, stores, transactions, users

class User(Document, users.BaseUser):
    password_hash: str
    class Settings:
        name = "users"

class Store(Document, stores.CreateStore):
    user = Link[User]
    class Settings:
        name = "stores"

class Transaction(Document, transactions.CreateTransaction):
    from_store = Link[Store]
    from_user = Link[User]
    class Settings:
        name = "transactions"

class Snapshot(Document, snapshots.CreateSnapshot):
    class Settings:
        name = "snapshots"

class Product(Document, products.CreateProduct):
    snapshot = Link[Snapshot]
    class Settings:
        name = "products"

class Billing(Document, billing.CreateBilling):
    from_transaction = Link[Transaction]
    class Settings:
        name = "billings"

class Selling(Document, selling.CreateSelling):
    from_transaction = Link[Transaction]
    product = Link[Product]
    class Settings:
        name = "sellings"







