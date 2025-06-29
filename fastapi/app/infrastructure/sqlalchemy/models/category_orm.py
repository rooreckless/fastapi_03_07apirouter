# モデル
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class CategoryORM(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, nullable=False)
    #カテゴリに属する商品一覧を取得する場合は↓が必要になる。
    # category対Item = 一対多
    items: Mapped[list["ItemORM"]] = relationship(back_populates="category")