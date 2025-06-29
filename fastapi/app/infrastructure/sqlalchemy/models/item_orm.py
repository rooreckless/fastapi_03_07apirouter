from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ItemORM(Base):
    __tablename__ = "items"

    # item_id = Column(Integer, primary_key=True, index=True)
    # item_name = Column(String, nullable=False)
    # category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)

    # # category = relationship("CategoryORM")
    # category = relationship("CategoryORM", back_populates="items")
    item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)

    category: Mapped["CategoryORM"] = relationship(back_populates="items")
