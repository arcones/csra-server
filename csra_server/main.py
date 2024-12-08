from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from csra_server import models
from csra_server.database import SessionLocal, create_database
from csra_server.schemas import ItemResponse

async def lifespan(app: FastAPI):
    """Lifespan function for app startup and shutdown."""
    # Startup actions
    await create_database()
    yield  # You can perform shutdown actions here if needed
app = FastAPI(lifespan=lifespan)

# Dependency for database session
async def get_db():
    async with SessionLocal() as db:
        yield db

# Get all items
@app.get("/items/", response_model=list[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    return items




#
#
#
# # Create an Item
# @app.post("/items/", response_model=ItemResponse)
# async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
#     db_item = models.Item(name=item.name, description=item.description)
#     db.add(db_item)
#     await db.commit()  # Asynchronous commit
#     await db.refresh(db_item)  # Refresh asynchronously
#     return db_item
#
# # Get an Item by ID
# @app.get("/items/{item_id}", response_model=ItemResponse)
# async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
#     db_item = result.scalars().first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item
#
# # Update an Item by ID
# @app.put("/items/{item_id}", response_model=ItemResponse)
# async def update_item(item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
#     db_item = result.scalars().first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     db_item.name = item.name
#     db_item.description = item.description
#     await db.commit()  # Asynchronous commit
#     await db.refresh(db_item)  # Refresh asynchronously
#     return db_item
#
# # Delete an Item by ID
# @app.delete("/items/{item_id}", response_model=ItemResponse)
# async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
#     db_item = result.scalars().first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     await db.delete(db_item)
#     await db.commit()  # Asynchronous commit
#     return db_item
