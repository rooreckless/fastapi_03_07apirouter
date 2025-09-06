"""
ユーザー認証ユースケース
"""
from typing import Union

from app.abstract_repository.user_repository import UserRepository
from app.domain.user.value_objects import MailAddress
from app.dto.user_dto import UserLoginDTO, TokenDTO
from app.core.security import verify_password
from app.core.jwt import create_access_token


class AuthenticateUserUseCase:
    """ユーザー認証ユースケース"""
    
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    async def execute(self, dto: UserLoginDTO) -> Union[TokenDTO, None]:
        """ユーザー認証処理
        
        Args:
            dto: ログイン情報DTO
            
        Returns:
            TokenDTO | None: 認証成功時はトークン、失敗時はNone
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"認証試行: メールアドレス={dto.mail_address}")
        
        # メールアドレスでユーザーを取得
        mail_address = MailAddress(dto.mail_address)
        user = await self.user_repository.get_by_mail_address(mail_address)
        
        if user is None:
            logger.warning(f"ユーザーが見つかりません: {dto.mail_address}")
            return None
        
        logger.info(f"ユーザー見つかりました: ID={user.id}, アクティブ={user.is_active}")
        
        # パスワード検証
        password_valid = verify_password(dto.password, user.hashed_password.value)
        logger.info(f"パスワード検証結果: {password_valid}")
        
        if not password_valid:
            logger.warning("パスワードが一致しません")
            return None
        
        # アクティブユーザーチェック
        if not user.is_active:
            logger.warning("非アクティブユーザーです")
            return None
        
        # JWTトークン生成
        access_token = create_access_token(sub=str(user.id))
        logger.info("認証成功、トークン生成完了")
        
        return TokenDTO(
            access_token=access_token,
            token_type="bearer"
        )
