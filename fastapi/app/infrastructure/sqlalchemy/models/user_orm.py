"""
ユーザーORMモデル
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class UserORM(Base):
    """ユーザーORM"""
    
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    mail_address = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<UserORM(user_id={self.user_id}, mail_address='{self.mail_address}', is_active={self.is_active})>"
