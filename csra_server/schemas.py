from pydantic import BaseModel

# Schema for creating a new item
class ItemCreate(BaseModel):
    name: str
    description: str

# Schema for updating an existing item
class ItemUpdate(BaseModel):
    name: str
    description: str

# Schema for reading an item (response model)
class Item(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True  # Enable compatibility with ORM objects
