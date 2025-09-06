"""
ユーザーマッパー - ドメインエンティティとORMモデル間の変換
"""
from typing import List

from app.domain.user.user import User
from app.domain.user.value_objects import UserId, MailAddress, HashedPassword, FullName
from app.infrastructure.sqlalchemy.models.user_orm import UserORM


class UserMapper:
    """ユーザーエンティティとORMモデル間の変換を行うマッパー"""
    
    @staticmethod
    def to_domain(orm: UserORM) -> User:
        """ORMモデルからドメインエンティティに変換
        
        Args:
            orm: UserORMインスタンス
            
        Returns:
            User: ユーザードメインエンティティ
        """
        return User(
            user_id=UserId(orm.user_id) if orm.user_id else None,
            mail_address=MailAddress(orm.mail_address),
            hashed_password=HashedPassword(orm.hashed_password),
            full_name=FullName(orm.full_name),
            is_active=orm.is_active,
            is_superuser=orm.is_superuser,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    @staticmethod
    def to_orm(domain: User) -> UserORM:
        """ドメインエンティティからORMモデルに変換
        
        Args:
            domain: ユーザードメインエンティティ
            
        Returns:
            UserORM: ORMモデルインスタンス
        """
        return UserORM(
            user_id=domain.user_id.value if domain.user_id else None,
            mail_address=domain.mail_address.value,
            hashed_password=domain.hashed_password.value,
            full_name=domain.full_name.value,
            is_active=domain.is_active,
            is_superuser=domain.is_superuser,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    @staticmethod
    def to_domain_list(orm_list: List[UserORM]) -> List[User]:
        """ORMモデルリストからドメインエンティティリストに変換
        
        Args:
            orm_list: UserORMインスタンスのリスト
            
        Returns:
            List[User]: ユーザードメインエンティティのリスト
        """
        return [UserMapper.to_domain(orm) for orm in orm_list]
