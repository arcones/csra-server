from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from csra_server import models
from csra_server.database import SessionLocal, create_database
from csra_server.schemas import ItemResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    yield
app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as db:
        yield db

@app.get("/items/", response_model=list[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    return items