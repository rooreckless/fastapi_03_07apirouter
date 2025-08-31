"""
ユーザー取得ユースケース
"""
from typing import Union

from app.abstract_repository.user_repository import UserRepository
from app.domain.user.value_objects import UserId
from app.dto.user_dto import UserReadDTO


class GetUserUseCase:
    """ユーザー取得ユースケース"""
    
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    async def execute(self, user_id: int) -> Union[UserReadDTO, None]:
        """ユーザー取得処理
        
        Args:
            user_id: 取得するユーザーのID
            
        Returns:
            UserReadDTO | None: 見つかったユーザー情報、存在しない場合はNone
        """
        user_id_vo = UserId(user_id)
        user = await self.user_repository.get_by_id(user_id_vo)
        
        if user is None:
            return None
        
        return UserReadDTO(
            user_id=user.id,
            mail_address=user.mail_address.value,
            full_name=user.full_name.value,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
