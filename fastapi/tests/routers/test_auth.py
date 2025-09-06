# tests/routers/test_auth.py
"""
認証ルーター用のテストケース
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.auth import get_user_repository, get_current_user
from app.dto.user_dto import UserCreateDTO, UserReadDTO, TokenDTO
from app.infrastructure.sqlalchemy.repo_imples.user_repo_impl import SQLAlchemyUserRepository


@pytest.fixture
def mock_user_repo():
    """モックされたユーザーリポジトリ"""
    return AsyncMock(spec=SQLAlchemyUserRepository)


@pytest.fixture
def sample_user_read_dto():
    """テスト用のユーザー読み込みDTO"""
    return UserReadDTO(
        user_id=1,
        mail_address="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )


@pytest.fixture
def sample_token_dto():
    """テスト用のトークンDTO"""
    return TokenDTO(access_token="test_token", token_type="bearer")


@pytest.fixture
def sample_user_create_dto():
    """テスト用のユーザー作成DTO"""
    return UserCreateDTO(
        mail_address="new@example.com",
        password="password123",
        full_name="New User"
    )


class TestGetUserRepository:
    """ユーザーリポジトリ依存性注入のテスト"""

    def test_get_user_repository_creates_instance(self):
        """正常にSQLAlchemyUserRepositoryインスタンスを作成することを確認"""
        mock_db = Mock()
        result = get_user_repository(mock_db)
        assert isinstance(result, SQLAlchemyUserRepository)
        assert result.db == mock_db


class TestRegisterEndpoint:
    """ユーザー登録エンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_register_success(self, mock_user_repo, sample_user_create_dto, sample_user_read_dto):
        """ユーザー登録が成功する場合のテスト"""
        with patch('app.routers.auth.CreateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = sample_user_read_dto
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import register
            result = await register(sample_user_create_dto, mock_user_repo)
            
            assert result == sample_user_read_dto
            mock_usecase_class.assert_called_once_with(mock_user_repo)
            mock_usecase.execute.assert_called_once_with(sample_user_create_dto)

    @pytest.mark.asyncio
    async def test_register_value_error_returns_400(self, mock_user_repo, sample_user_create_dto):
        """バリデーションエラーが発生した場合に400エラーを返すテスト"""
        with patch('app.routers.auth.CreateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.side_effect = ValueError("メールアドレスが無効です")
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import register
            with pytest.raises(HTTPException) as exc_info:
                await register(sample_user_create_dto, mock_user_repo)
            
            assert exc_info.value.status_code == 400
            assert "メールアドレスが無効です" in str(exc_info.value.detail)


class TestLoginEndpoint:
    """アプリ用ログインエンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_login_success(self, mock_user_repo, sample_token_dto):
        """ログインが成功する場合のテスト"""
        with patch('app.routers.auth.AuthenticateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = sample_token_dto
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import login
            result = await login("test@example.com", "password", mock_user_repo)
            
            assert result == sample_token_dto
            mock_usecase.execute.assert_called_once()
            call_args = mock_usecase.execute.call_args[0][0]
            assert call_args.mail_address == "test@example.com"
            assert call_args.password == "password"

    @pytest.mark.asyncio
    async def test_login_invalid_credentials_returns_401(self, mock_user_repo):
        """認証失敗時に401エラーを返すテスト"""
        with patch('app.routers.auth.AuthenticateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = None
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import login
            with pytest.raises(HTTPException) as exc_info:
                await login("test@example.com", "wrong_password", mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid credentials"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


class TestTokenEndpoint:
    """OAuth2トークンエンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_token_success(self, mock_user_repo, sample_token_dto):
        """OAuth2トークン取得が成功する場合のテスト"""
        mock_form = Mock(spec=OAuth2PasswordRequestForm)
        mock_form.username = "test@example.com"
        mock_form.password = "password"
        
        with patch('app.routers.auth.AuthenticateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = sample_token_dto
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import token
            result = await token(mock_form, mock_user_repo)
            
            assert result == sample_token_dto
            mock_usecase.execute.assert_called_once()
            call_args = mock_usecase.execute.call_args[0][0]
            assert call_args.mail_address == "test@example.com"
            assert call_args.password == "password"

    @pytest.mark.asyncio
    async def test_token_invalid_credentials_returns_401(self, mock_user_repo):
        """OAuth2認証失敗時に401エラーを返すテスト"""
        mock_form = Mock(spec=OAuth2PasswordRequestForm)
        mock_form.username = "test@example.com"
        mock_form.password = "wrong_password"
        
        with patch('app.routers.auth.AuthenticateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = None
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import token
            with pytest.raises(HTTPException) as exc_info:
                await token(mock_form, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid credentials"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


class TestGetCurrentUser:
    """現在のユーザー取得関数のテスト"""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, mock_user_repo, sample_user_read_dto):
        """有効なトークンで現在のユーザーを正常に取得するテスト"""
        test_token = "valid_token"
        
        with patch('app.routers.auth.decode_token') as mock_decode, \
             patch('app.routers.auth.GetUserUseCase') as mock_usecase_class:
            
            mock_decode.return_value = {"sub": "1"}
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = sample_user_read_dto
            mock_usecase_class.return_value = mock_usecase
            
            result = await get_current_user(test_token, mock_user_repo)
            
            assert result == sample_user_read_dto
            mock_decode.assert_called_once_with(test_token)
            mock_usecase.execute.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token_raises_401(self, mock_user_repo):
        """無効なトークンで401エラーが発生するテスト"""
        test_token = "invalid_token"
        
        with patch('app.routers.auth.decode_token') as mock_decode:
            mock_decode.side_effect = Exception("Invalid token")
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid or expired token"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    @pytest.mark.asyncio
    async def test_get_current_user_user_not_found_raises_401(self, mock_user_repo):
        """ユーザーが見つからない場合に401エラーが発生するテスト"""
        test_token = "valid_token"
        
        with patch('app.routers.auth.decode_token') as mock_decode, \
             patch('app.routers.auth.GetUserUseCase') as mock_usecase_class:
            
            mock_decode.return_value = {"sub": "1"}
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = None
            mock_usecase_class.return_value = mock_usecase
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Inactive or missing user"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    @pytest.mark.asyncio
    async def test_get_current_user_inactive_user_raises_401(self, mock_user_repo):
        """非アクティブユーザーで401エラーが発生するテスト"""
        test_token = "valid_token"
        inactive_user = UserReadDTO(
            user_id=1,
            mail_address="test@example.com",
            full_name="Test User",
            is_active=False,
            is_superuser=False
        )
        
        with patch('app.routers.auth.decode_token') as mock_decode, \
             patch('app.routers.auth.GetUserUseCase') as mock_usecase_class:
            
            mock_decode.return_value = {"sub": "1"}
            mock_usecase = AsyncMock()
            mock_usecase.execute.return_value = inactive_user
            mock_usecase_class.return_value = mock_usecase
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Inactive or missing user"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_user_id_raises_401(self, mock_user_repo):
        """無効なユーザーIDで401エラーが発生するテスト"""
        test_token = "valid_token"
        
        with patch('app.routers.auth.decode_token') as mock_decode:
            mock_decode.return_value = {"sub": "invalid_id"}
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid or expired token"
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


class TestGetMeEndpoint:
    """現在のユーザー情報取得エンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_get_me_returns_current_user(self, sample_user_read_dto):
        """現在のユーザー情報を正常に返すテスト"""
        from app.routers.auth import get_me
        result = await get_me(sample_user_read_dto)
        assert result == sample_user_read_dto


class TestEdgeCases:
    """エッジケースのテスト"""

    @pytest.mark.asyncio
    async def test_login_empty_credentials(self, mock_user_repo):
        """空の認証情報でのログインテスト"""
        with patch('app.routers.auth.UserLoginDTO') as mock_dto_class:
            mock_dto_class.side_effect = ValueError("メールアドレスが必須です")
            
            from app.routers.auth import login
            with pytest.raises(ValueError):
                await login("", "", mock_user_repo)

    @pytest.mark.asyncio
    async def test_token_empty_form_data(self, mock_user_repo):
        """空のフォームデータでのOAuth2トークンテスト"""
        mock_form = Mock(spec=OAuth2PasswordRequestForm)
        mock_form.username = ""
        mock_form.password = ""
        
        with patch('app.routers.auth.UserLoginDTO') as mock_dto_class:
            mock_dto_class.side_effect = ValueError("メールアドレスが必須です")
            
            from app.routers.auth import token
            with pytest.raises(ValueError):
                await token(mock_form, mock_user_repo)

    @pytest.mark.asyncio
    async def test_get_current_user_token_decode_value_error(self, mock_user_repo):
        """トークンデコード時のValueErrorのテスト"""
        test_token = "malformed_token"
        
        with patch('app.routers.auth.decode_token') as mock_decode:
            mock_decode.side_effect = ValueError("Malformed token")
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_get_current_user_empty_token(self, mock_user_repo):
        """空のトークンでのテスト"""
        test_token = ""
        
        with patch('app.routers.auth.decode_token') as mock_decode:
            mock_decode.side_effect = Exception("Empty token")
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(test_token, mock_user_repo)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid or expired token"

    @pytest.mark.asyncio
    async def test_register_unexpected_exception(self, mock_user_repo, sample_user_create_dto):
        """予期しない例外が発生した場合のテスト（再発生確認）"""
        with patch('app.routers.auth.CreateUserUseCase') as mock_usecase_class:
            mock_usecase = AsyncMock()
            mock_usecase.execute.side_effect = RuntimeError("Unexpected error")
            mock_usecase_class.return_value = mock_usecase
            
            from app.routers.auth import register
            with pytest.raises(RuntimeError, match="Unexpected error"):
                await register(sample_user_create_dto, mock_user_repo)
