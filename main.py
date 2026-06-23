from contextlib import asynccontextmanager

from fastapi_pagination import add_pagination
from db import server

from fastapi import FastAPI
from routers import billing, products, selling, snapshots, stores, transactions, users

@asynccontextmanager
async def lifespan(_: FastAPI):
    await server.initialize()
    
    yield

app = FastAPI(lifespan=lifespan)

add_pagination(app)

app.include_router(billing.router, tags=["Billing"])
app.include_router(products.router, tags=["Products"])
app.include_router(selling.router, tags=["Selling"])
app.include_router(snapshots.router, tags=["Snapshots"])
app.include_router(stores.router, tags=["Stores"])
app.include_router(transactions.router, tags=["Transactions"])
app.include_router(users.router, tags=["Users"])