from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class CategoryORM(Base):
    __tablename__ = "categories"

    # category_id = Column(Integer, primary_key=True, index=True)
    # category_name = Column(String, nullable=False)

    # items = relationship("ItemORM", back_populates="category")
    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, nullable=False)

    items: Mapped[list["ItemORM"]] = relationship(back_populates="category")