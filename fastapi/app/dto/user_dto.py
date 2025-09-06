"""
ユーザー関連のDTO（Data Transfer Object）
"""
from __future__ import annotations
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Union
from datetime import datetime
import re


class UserCreateDTO(BaseModel):
    """ユーザー作成DTO"""
    
    mail_address: str
    password: str
    full_name: Union[str, None] = None
    is_active: bool = True
    is_superuser: bool = False
    
    @field_validator('mail_address')
    @classmethod
    def validate_mail_address(cls, v: str) -> str:
        if not v:
            raise ValueError('Mail address cannot be empty')
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid mail address format')
        
        if len(v) > 254:
            raise ValueError('Mail address is too long')
        
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError('Password cannot be empty')
        
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if len(v) > 128:
            raise ValueError('Password is too long')
        
        return v
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: Union[str, None]) -> Union[str, None]:
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('Full name cannot be empty or whitespace only')
            
            if len(v) > 100:
                raise ValueError('Full name is too long (max 100 characters)')
        
        return v


class UserUpdateDTO(BaseModel):
    """ユーザー更新DTO"""
    
    full_name: Union[str, None] = None
    is_active: Union[bool, None] = None
    is_superuser: Union[bool, None] = None
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: Union[str, None]) -> Union[str, None]:
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('Full name cannot be empty or whitespace only')
            
            if len(v) > 100:
                raise ValueError('Full name is too long (max 100 characters)')
        
        return v


class UserReadDTO(BaseModel):
    """ユーザー読み取りDTO"""
    
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    mail_address: str
    full_name: Union[str, None]
    is_active: bool
    is_superuser: bool
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class UserLoginDTO(BaseModel):
    """ユーザーログインDTO"""
    
    mail_address: str
    password: str
    
    @field_validator('mail_address')
    @classmethod
    def validate_mail_address(cls, v: str) -> str:
        if not v:
            raise ValueError('Mail address cannot be empty')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError('Password cannot be empty')
        return v


class TokenDTO(BaseModel):
    """トークンDTO"""
    
    access_token: str
    token_type: str = "bearer"


class UserPasswordChangeDTO(BaseModel):
    """パスワード変更DTO"""
    
    current_password: str
    new_password: str
    
    @field_validator('current_password')
    @classmethod
    def validate_current_password(cls, v: str) -> str:
        if not v:
            raise ValueError('Current password cannot be empty')
        return v
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if not v:
            raise ValueError('New password cannot be empty')
        
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        
        if len(v) > 128:
            raise ValueError('New password is too long')
        
        return v
