from typing import TYPE_CHECKING
from sqlalchemy import String
# Mappedを使う新しい書き方にする
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# 中間テーブルもimportして、ItemORMで利用できるようにする
from app.infrastructure.sqlalchemy.models.item_category_association import item_category

if TYPE_CHECKING:
    from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM


class ItemORM(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String, nullable=False)
    # カテゴリは、listとして扱う。
    # relationshipを使って、CategoryORMとの多対多の関係を定義し、直接の相手はCategoryORMではなく、item_categoryという中間テーブルを使う。
    categories: Mapped[list["CategoryORM"]] = relationship(
        "CategoryORM",  # 紐づける相手のクラス名(文字列で指定)
        secondary=item_category,    # 中間テーブルを指定
        back_populates="items"  # CategoryORM 側の「items」フィールドと双方向に関連付け = CategoryORM側で「items」フィールドを用意する必要がある。
    )
