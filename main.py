from contextlib import asynccontextmanager
from db import server

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await server.initialize()
    
    yield

app = FastAPI()

