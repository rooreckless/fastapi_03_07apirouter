
from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    item_name: str
    category_id: int