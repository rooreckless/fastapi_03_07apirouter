from sqlalchemy import Column, Integer, String, ForeignKey
# Mappedやmapped_columnを使う方が新しい書き方であるので、このファイルは現状古い方の書き方
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ItemORM(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    # Item対category = 多対一
    category = relationship("CategoryORM")
    
    # item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # item_name: Mapped[str] = mapped_column(String, nullable=False)
    # category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)

    # category: Mapped["CategoryORM"] = relationship(back_populates="items")
