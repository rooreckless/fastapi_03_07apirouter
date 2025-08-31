# app/core/security.py
from passlib.context import CryptContext

# bcrypt 4.2以降の互換性問題を回避
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12  # bcryptのデフォルト設定を明示的に指定
)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False
