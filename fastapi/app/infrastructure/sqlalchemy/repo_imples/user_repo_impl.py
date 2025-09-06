"""
ユーザーリポジトリの実装
"""
from typing import Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.abstract_repository.user_repository import UserRepository
from app.domain.user.user import User
from app.domain.user.value_objects import UserId, MailAddress
from app.infrastructure.sqlalchemy.models.user_orm import UserORM
from app.infrastructure.sqlalchemy.mappers.user_mapper import UserMapper


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemyを使用したユーザーリポジトリの実装
    
    データベースアクセスとORM変換を担当
    """
    
    def __init__(self, db: AsyncSession) -> None:
        """
        Args:
            db: SQLAlchemyの非同期セッション
        """
        self.db = db
        self.mapper = UserMapper()
    
    async def save(self, user: User) -> None:
        """ユーザーを保存
        
        新規ユーザーの場合は新しいレコードを作成し、
        既存ユーザーの場合は更新を行う
        
        Args:
            user: 保存するユーザーエンティティ
        """
        # Mapperを使用してドメインエンティティをORMモデルに変換
        orm = self.mapper.to_orm(user)
        
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        user.id = orm.user_id   # エンティティへIDを返す
    
    async def get_by_id(self, user_id: UserId) -> Union[User, None]:
        """IDでユーザーを取得
        
        Args:
            user_id: 取得するユーザーのID
            
        Returns:
            User | None: 見つかったユーザーエンティティ、存在しない場合はNone
        """
        result = await self.db.execute(
            select(UserORM).filter(UserORM.user_id == user_id.value)
        )
        orm = result.scalar_one_or_none()
        
        if orm is None:
            return None
        
        # Mapperを使用してORMモデルをドメインエンティティに変換
        return self.mapper.to_domain(orm)
    
    async def get_by_mail_address(self, mail_address: MailAddress) -> Union[User, None]:
        """メールアドレスでユーザーを取得
        
        Args:
            mail_address: 取得するユーザーのメールアドレス
            
        Returns:
            User | None: 見つかったユーザーエンティティ、存在しない場合はNone
        """
        result = await self.db.execute(
            select(UserORM).filter(UserORM.mail_address == mail_address.value)
        )
        orm = result.scalar_one_or_none()
        
        if orm is None:
            return None
        
        # Mapperを使用してORMモデルをドメインエンティティに変換
        return self.mapper.to_domain(orm)
    
    async def list_all(self) -> List[User]:
        """全ユーザーをリスト形式で取得
        
        Returns:
            List[User]: ユーザーエンティティのリスト
        """
        result = await self.db.execute(select(UserORM))
        orm_list = result.scalars().all()
        
        # Mapperを使用してORMモデルリストをドメインエンティティリストに変換
        return self.mapper.to_domain_list(orm_list)
    
    async def next_identifier(self) -> UserId:
        """次のユーザーIDを生成
        
        現在の最大IDに1を加えた値を返す
        
        Returns:
            UserId: 次に使用するユーザーID
        """
        result = await self.db.execute(
            select(func.max(UserORM.user_id))
        )
        max_id = result.scalar()
        next_id = 1 if max_id is None else max_id + 1
        return UserId(next_id)
    
    async def update(self, user: User) -> Union[User, None]:
        """ユーザーを更新
        
        Args:
            user: 更新するユーザーエンティティ
            
        Returns:
            User | None: 更新されたユーザーエンティティ、存在しない場合はNone
        """
        if user.user_id is None:
            return None
        
        # 既存のユーザーを取得
        result = await self.db.execute(
            select(UserORM).filter(UserORM.user_id == user.user_id.value)
        )
        orm = result.scalar_one_or_none()
        
        if orm is None:
            return None
        
        # フィールドを更新
        orm.mail_address = user.mail_address.value
        orm.hashed_password = user.hashed_password.value
        orm.full_name = user.full_name.value
        orm.is_active = user.is_active
        orm.is_superuser = user.is_superuser
        
        await self.db.commit()
        await self.db.refresh(orm)
        
        # Mapperを使用してORMモデルをドメインエンティティに変換して返す
        return self.mapper.to_domain(orm)
    
    async def delete(self, user_id: UserId) -> bool:
        """ユーザーを削除
        
        Args:
            user_id: 削除するユーザーのID
            
        Returns:
            bool: 削除が成功した場合はTrue、存在しない場合はFalse
        """
        result = await self.db.execute(
            select(UserORM).filter(UserORM.user_id == user_id.value)
        )
        orm = result.scalar_one_or_none()
        
        if orm is None:
            return False
        
        await self.db.delete(orm)
        await self.db.commit()
        return True
