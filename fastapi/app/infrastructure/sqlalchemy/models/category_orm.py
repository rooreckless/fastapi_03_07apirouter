# モデル
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# 中間テーブルもimportして、ItemORMで利用できるようにする
from app.infrastructure.sqlalchemy.models.item_category_association import item_category

if TYPE_CHECKING:
    from app.infrastructure.sqlalchemy.models.item_orm import ItemORM


class CategoryORM(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, nullable=False)
    # カテゴリに属する商品一覧を取得する場合は↓が必要になる。
    # category対Item = 一対多
    items: Mapped[list["ItemORM"]] = relationship(
        "ItemORM",  # 紐づける相手のクラス名(文字列で指定)
        secondary=item_category,   # 中間テーブルを指定
        back_populates="categories"  # ItemsORM側の「categories」フィールドと双方向に関連付け
    )
