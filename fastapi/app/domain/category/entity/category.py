# ①ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/category/entity/category.py
from typing import Optional
from datetime import datetime


class Category:
    def __init__(
        self, 
        category_id: int, 
        name: str,
        created_by: Optional[int] = None,
        updated_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        if category_id < 0:
            raise ValueError("カテゴリIDは0以上でなければなりません")
        self.id = category_id
        self.name = name
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
