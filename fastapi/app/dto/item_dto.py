# app/dto/item_dto.py
# スキーマ =⑤のエンドポイントで引数に入れられる
from pydantic import BaseModel, ConfigDict
from typing import List

class ItemBase(BaseModel):
    item_name: str
    category_ids: List[int] | None

class ItemCreateDTO(ItemBase):
    pass
class ItemUpdateDTO(ItemBase):
    pass
class ItemUpdateNameDTO(BaseModel):
    # ItemのNameだけを更新する際に使う
    item_name: str

class ItemReadDTO(ItemBase):
    item_id: int
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True