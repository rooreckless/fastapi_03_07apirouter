"""
ユーザードメインエンティティ
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from datetime import datetime

from .value_objects import UserId, MailAddress, HashedPassword, FullName


@dataclass
class User:
    """ユーザーエンティティ"""
    
    user_id: Union[UserId, None]
    mail_address: MailAddress
    hashed_password: HashedPassword
    full_name: FullName
    is_active: bool = True
    is_superuser: bool = False
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    created_by: Union[UserId, None] = None
    updated_by: Union[UserId, None] = None
    
    def __post_init__(self) -> None:
        """エンティティレベルのバリデーション"""
        # 既に値オブジェクトでバリデーション済みなので、
        # ここではエンティティレベルのビジネスルールのみ
        pass
    
    @property
    def id(self) -> Union[int, None]:
        """ユーザーIDを整数で取得"""
        return self.user_id.value if self.user_id else None
    
    @id.setter
    def id(self, value: int) -> None:
        """ユーザーIDを設定"""
        self.user_id = UserId(value)
    
    def is_authenticated(self) -> bool:
        """認証済みユーザーかどうか"""
        return self.user_id is not None and self.is_active
    
    def can_access_admin_features(self) -> bool:
        """管理者機能にアクセス可能かどうか"""
        return self.is_authenticated() and self.is_superuser
    
    def update_profile(self, full_name: Union[str, None]) -> None:
        """プロフィール更新"""
        self.full_name = FullName(full_name)
    
    def deactivate(self) -> None:
        """ユーザーを無効化"""
        self.is_active = False
    
    def activate(self) -> None:
        """ユーザーを有効化"""
        self.is_active = True
    
    def make_superuser(self) -> None:
        """スーパーユーザーにする"""
        self.is_superuser = True
    
    def revoke_superuser(self) -> None:
        """スーパーユーザー権限を取り消す"""
        self.is_superuser = False
    
    def __eq__(self, other: object) -> bool:
        """等価性の判定はユーザーIDで行う"""
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id
    
    def __hash__(self) -> int:
        """ハッシュ値はユーザーIDで計算"""
        return hash(self.user_id) if self.user_id else hash(id(self))
