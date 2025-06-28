
# from pydantic import BaseModel

# class Item(BaseModel):
#     item_id: int
#     item_name: str
#     category_id: int

from pydantic import BaseModel

class ItemBase(BaseModel):
    item_name: str
    category_id: int

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    item_id: int

    class Config:
        orm_mode = True
