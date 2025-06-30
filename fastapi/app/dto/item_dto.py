# app/dto/item_dto.py
# スキーマ =⑤のエンドポイントで引数に入れられる
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    item_name: str
    category_id: int

class ItemCreateDTO(ItemBase):
    pass
class ItemUpdateDTO(ItemBase):
    pass

class ItemReadDTO(ItemBase):
    item_id: int
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True