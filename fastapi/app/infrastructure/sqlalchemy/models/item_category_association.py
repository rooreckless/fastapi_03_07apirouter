# 中間テーブル itemとcateogoryの多対多の関係を表す
# しかし、ItemOrmとかのようにOrmクラスを定義する必要はない。直接sqlalchemyのTableを使って定義する。
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

item_category = Table(
    "item_category",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.item_id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), primary_key=True)
)
