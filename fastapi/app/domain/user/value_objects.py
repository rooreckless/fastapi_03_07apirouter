"""
ユーザードメインの値オブジェクト
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class UserId:
    """ユーザーIDの値オブジェクト"""
    
    value: int
    
    def __post_init__(self) -> None:
        """バリデーション"""
        if self.value <= 0:
            raise ValueError("User ID must be a positive integer")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class MailAddress:
    """メールアドレスの値オブジェクト"""
    
    value: str
    
    def __post_init__(self) -> None:
        """バリデーション"""
        if not self.value:
            raise ValueError("Mail address cannot be empty")
        
        if not self._is_valid_email(self.value):
            raise ValueError("Invalid mail address format")
        
        if len(self.value) > 254:  # RFC 5321制限
            raise ValueError("Mail address is too long")
    
    def _is_valid_email(self, email: str) -> bool:
        """メールアドレスの基本的なバリデーション"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __str__(self) -> str:
        return self.value
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class HashedPassword:
    """ハッシュ化されたパスワードの値オブジェクト"""
    
    value: str
    
    def __post_init__(self) -> None:
        """バリデーション"""
        if not self.value:
            raise ValueError("Hashed password cannot be empty")
        
        # bcryptハッシュの基本的な形式チェック
        if not self.value.startswith('$2b$'):
            raise ValueError("Invalid hashed password format")
    
    def __str__(self) -> str:
        return self.value
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class FullName:
    """フルネームの値オブジェクト"""
    
    value: Union[str, None]
    
    def __post_init__(self) -> None:
        """バリデーション"""
        if self.value is not None:
            if len(self.value.strip()) == 0:
                raise ValueError("Full name cannot be empty or whitespace only")
            
            if len(self.value) > 100:
                raise ValueError("Full name is too long (max 100 characters)")
    
    def __str__(self) -> str:
        return self.value if self.value is not None else ""
    
    def __hash__(self) -> int:
        return hash(self.value)
