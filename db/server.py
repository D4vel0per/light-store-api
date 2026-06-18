from pymongo.asynchronous.mongo_client import AsyncMongoClient
from beanie import init_beanie
from db.documents import Billing, Product, Selling, Snapshot, Store, Transaction, User

async def initialize ():
    client = AsyncMongoClient()
    DB = client["light-store-db"]

    await init_beanie(database=DB, document_models=[
        Billing,
        Product,
        Selling,
        Snapshot,
        Store,
        Transaction,
        User
    ])

