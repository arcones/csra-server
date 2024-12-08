from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

#
#
# # Schema for creating a new item
# class ItemCreate(BaseModel):
#     name: str
#     description: str
#
# # Schema for updating an existing item
# class ItemUpdate(BaseModel):
#     name: str
#     description: str
#
# # Schema for reading an item (response model)
