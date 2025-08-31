# モデル
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base

# 中間テーブルもimportして、ItemORMで利用できるようにする
from app.infrastructure.sqlalchemy.models.item_category_association import item_category

if TYPE_CHECKING:
    from app.infrastructure.sqlalchemy.models.item_orm import ItemORM


class CategoryORM(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)
    
    # カテゴリに属する商品一覧を取得する場合は↓が必要になる。
    # category対Item = 一対多
    items: Mapped[list["ItemORM"]] = relationship(
        "ItemORM",  # 紐づける相手のクラス名(文字列で指定)
        secondary=item_category,   # 中間テーブルを指定
        back_populates="categories"  # ItemsORM側の「categories」フィールドと双方向に関連付け
    )
