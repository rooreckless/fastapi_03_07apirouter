"""
AuthenticateUserUseCaseのテスト
"""
import pytest
from unittest.mock import AsyncMock, patch

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.abstract_repository.user_repository import UserRepository
from app.domain.user.user import User
from app.domain.user.value_objects import UserId, MailAddress, HashedPassword, FullName
from app.dto.user_dto import UserLoginDTO, TokenDTO


class TestAuthenticateUserUseCase:
    """AuthenticateUserUseCaseのテスト"""
    
    def test_init_with_repository(self):
        """正常系: リポジトリでユースケースを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        
        # Act
        use_case = AuthenticateUserUseCase(mock_repo)
        
        # Assert
        assert use_case.user_repository == mock_repo
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    @patch('app.usecases.user.authenticate_user.create_access_token')
    async def test_execute_authentication_success(self, mock_create_token, mock_verify_password):
        """正常系: 認証が成功する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = True
        mock_create_token.return_value = "mock_token"
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="password123"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is not None
        assert isinstance(result, TokenDTO)
        assert result.access_token == "mock_token"
        assert result.token_type == "bearer"
        mock_repo.get_by_mail_address.assert_called_once()
        mock_verify_password.assert_called_once()
        mock_create_token.assert_called_once_with(sub="1")
    
    @pytest.mark.anyio
    async def test_execute_user_not_found(self):
        """正常系: ユーザーが見つからない場合Noneを返す"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        mock_repo.get_by_mail_address.return_value = None
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="nonexistent@example.com",
            password="password123"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is None
        mock_repo.get_by_mail_address.assert_called_once()
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    async def test_execute_invalid_password(self, mock_verify_password):
        """正常系: 無効なパスワードの場合Noneを返す"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = False
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="wrong_password"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is None
        mock_repo.get_by_mail_address.assert_called_once()
        mock_verify_password.assert_called_once()
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    async def test_execute_inactive_user(self, mock_verify_password):
        """正常系: 非アクティブユーザーの場合Noneを返す"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=False,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = True
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="password123"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is None
        mock_repo.get_by_mail_address.assert_called_once()
        mock_verify_password.assert_called_once()
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    @patch('app.usecases.user.authenticate_user.create_access_token')
    async def test_execute_with_superuser(self, mock_create_token, mock_verify_password):
        """正常系: スーパーユーザーの認証が成功する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(99),
            mail_address=MailAddress("admin@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Admin User"),
            is_active=True,
            is_superuser=True
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = True
        mock_create_token.return_value = "admin_token"
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="admin@example.com",
            password="admin_password"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is not None
        assert isinstance(result, TokenDTO)
        assert result.access_token == "admin_token"
        assert result.token_type == "bearer"
        mock_create_token.assert_called_once_with(sub="99")
    
    @pytest.mark.anyio
    async def test_execute_with_empty_mail_address(self):
        """異常系: 空のメールアドレスでエラーが発生する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        use_case = AuthenticateUserUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(Exception):  # DTOレベルでバリデーションエラーが発生
            dto = UserLoginDTO(
                mail_address="",
                password="password123"
            )
            await use_case.execute(dto)
    
    @pytest.mark.anyio
    async def test_execute_with_invalid_mail_address_format(self):
        """異常系: 無効なメールアドレス形式でエラーが発生する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        use_case = AuthenticateUserUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(Exception):  # DTOレベルでバリデーションエラーが発生
            dto = UserLoginDTO(
                mail_address="invalid_email",
                password="password123"
            )
            await use_case.execute(dto)
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    @patch('app.usecases.user.authenticate_user.create_access_token')
    async def test_execute_with_japanese_full_name(self, mock_create_token, mock_verify_password):
        """エッジケース: 日本語の氏名を持つユーザーの認証"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(5),
            mail_address=MailAddress("japanese@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("田中太郎"),
            is_active=True,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = True
        mock_create_token.return_value = "japanese_token"
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="japanese@example.com",
            password="パスワード"
        )
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result is not None
        assert isinstance(result, TokenDTO)
        assert result.access_token == "japanese_token"
        mock_create_token.assert_called_once_with(sub="5")
    
    @pytest.mark.anyio
    async def test_execute_repository_error(self):
        """異常系: リポジトリでエラーが発生する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        mock_repo.get_by_mail_address.side_effect = Exception("Database error")
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await use_case.execute(dto)
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    async def test_execute_verify_password_error(self, mock_verify_password):
        """異常系: パスワード検証でエラーが発生する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.side_effect = Exception("Password verification error")
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Password verification error"):
            await use_case.execute(dto)
    
    @pytest.mark.anyio
    @patch('app.usecases.user.authenticate_user.verify_password')
    @patch('app.usecases.user.authenticate_user.create_access_token')
    async def test_execute_create_token_error(self, mock_create_token, mock_verify_password):
        """異常系: トークン生成でエラーが発生する"""
        # Arrange
        mock_repo = AsyncMock(spec=UserRepository)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        mock_repo.get_by_mail_address.return_value = user
        mock_verify_password.return_value = True
        mock_create_token.side_effect = Exception("Token creation error")
        
        use_case = AuthenticateUserUseCase(mock_repo)
        dto = UserLoginDTO(
            mail_address="test@example.com",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Token creation error"):
            await use_case.execute(dto)
