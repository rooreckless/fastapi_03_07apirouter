"""
ユーザーリポジトリの抽象定義
"""
from abc import ABC, abstractmethod
from typing import Union, List

from app.domain.user.user import User
from app.domain.user.value_objects import UserId, MailAddress


class UserRepository(ABC):
    """ユーザーリポジトリの抽象クラス
    
    ユーザーエンティティの永続化に関する操作を定義
    """
    
    @abstractmethod
    async def save(self, user: User) -> None:
        """ユーザーを保存"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> Union[User, None]:
        """IDでユーザーを取得"""
        pass
    
    @abstractmethod
    async def get_by_mail_address(self, mail_address: MailAddress) -> Union[User, None]:
        """メールアドレスでユーザーを取得"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[User]:
        """全ユーザーを取得"""
        pass
    
    @abstractmethod
    async def next_identifier(self) -> UserId:
        """次のユーザーIDを生成"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> Union[User, None]:
        """ユーザーを更新"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UserId) -> bool:
        """ユーザーを削除"""
        pass
