# ①ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/items/entity/item.py
from typing import Optional
from datetime import datetime


class Item:
    def __init__(
        self, 
        item_id: int, 
        name: str, 
        category_ids: list[int] | None = None,
        created_by: Optional[int] = None,
        updated_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = item_id
        self.name = name
        self.category_ids = category_ids
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
