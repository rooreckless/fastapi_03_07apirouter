"""
ユーザー作成ユースケース
"""
from app.abstract_repository.user_repository import UserRepository
from app.domain.user.user import User
from app.domain.user.value_objects import MailAddress, HashedPassword, FullName
from app.dto.user_dto import UserCreateDTO, UserReadDTO
from app.core.security import hash_password


class CreateUserUseCase:
    """ユーザー作成ユースケース"""
    
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    async def execute(self, dto: UserCreateDTO) -> UserReadDTO:
        """ユーザー作成処理
        
        Args:
            dto: ユーザー作成DTO
            
        Returns:
            UserReadDTO: 作成されたユーザー情報
            
        Raises:
            ValueError: メールアドレスが既に登録済みの場合
        """
        # メールアドレス重複チェック
        mail_address = MailAddress(dto.mail_address)
        existing_user = await self.user_repository.get_by_mail_address(mail_address)
        if existing_user is not None:
            raise ValueError("Mail address is already registered")
        
        # パスワードをハッシュ化
        hashed_password = HashedPassword(hash_password(dto.password))
        
        # 次のIDを取得
        next_id = await self.user_repository.next_identifier()
        
        # ユーザーエンティティを作成
        user = User(
            user_id=next_id,
            mail_address=mail_address,
            hashed_password=hashed_password,
            full_name=FullName(dto.full_name),
            is_active=dto.is_active,
            is_superuser=dto.is_superuser
        )
        
        # 保存
        await self.user_repository.save(user)
        
        # DTOに変換して返す
        return UserReadDTO(
            user_id=user.id,
            mail_address=user.mail_address.value,
            full_name=user.full_name.value,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
