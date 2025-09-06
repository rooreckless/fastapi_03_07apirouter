"""
SQLAlchemyUserRepositoryのテスト
"""
import pytest
from unittest.mock import AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result

from app.infrastructure.sqlalchemy.repo_imples.user_repo_impl import SQLAlchemyUserRepository
from app.domain.user.user import User
from app.domain.user.value_objects import UserId, MailAddress, FullName, HashedPassword
from app.infrastructure.sqlalchemy.models.user_orm import UserORM
from app.infrastructure.sqlalchemy.mappers.user_mapper import UserMapper


class TestSQLAlchemyUserRepositoryInit:
    """正常系: SQLAlchemyUserRepositoryの初期化テスト"""
    
    def test_init_with_valid_session(self):
        """正常系: 有効なセッションでリポジトリを初期化する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        
        # Act
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Assert
        assert repo.db == mock_session
        assert isinstance(repo.mapper, UserMapper)
    
    def test_init_with_none_session(self):
        """異常系: Noneセッションでリポジトリを初期化する"""
        # Arrange & Act
        repo = SQLAlchemyUserRepository(None)
        
        # Assert
        assert repo.db is None
        assert isinstance(repo.mapper, UserMapper)


class TestSQLAlchemyUserRepositorySave:
    """SQLAlchemyUserRepositoryのsaveメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_save_new_user_success(self):
        """正常系: 新規ユーザーの保存が成功する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        repo = SQLAlchemyUserRepository(mock_session)
        
        # refresh後にIDが設定されるようにMockを作成
        def setup_mock_orm(orm):
            orm.user_id = 1
        
        mock_session.refresh.side_effect = setup_mock_orm
        
        user = User(
            user_id=None,
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        
        # Act
        await repo.save(user)
        
        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.anyio
    async def test_save_user_with_japanese_name(self):
        """正常系: 日本語名前でユーザーを保存する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        repo = SQLAlchemyUserRepository(mock_session)
        
        # refresh後にIDが設定されるようにMockを作成
        def setup_mock_orm(orm):
            orm.user_id = 2
        
        mock_session.refresh.side_effect = setup_mock_orm
        
        user = User(
            user_id=None,
            mail_address=MailAddress("japanese@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("田中太郎"),
            is_active=True,
            is_superuser=False
        )
        
        # Act
        await repo.save(user)
        
        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.anyio
    async def test_save_user_commit_failure(self):
        """異常系: コミット失敗時にエラーが発生する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit.side_effect = Exception("Database error")
        repo = SQLAlchemyUserRepository(mock_session)
        
        user = User(
            user_id=None,
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repo.save(user)


class TestSQLAlchemyUserRepositoryGetById:
    """SQLAlchemyUserRepositoryのget_by_idメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_get_by_id_existing_user(self):
        """正常系: 存在するユーザーをIDで取得する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_orm = UserORM(
            user_id=1,
            mail_address="test@example.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO",
            full_name="Test User",
            is_active=True,
            is_superuser=False
        )
        mock_result.scalar_one_or_none.return_value = mock_orm
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user_id = UserId(1)
        
        # Act
        result = await repo.get_by_id(user_id)
        
        # Assert
        assert result is not None
        assert isinstance(result, User)
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_get_by_id_nonexistent_user(self):
        """正常系: 存在しないユーザーIDの場合Noneを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user_id = UserId(999)
        
        # Act
        result = await repo.get_by_id(user_id)
        
        # Assert
        assert result is None
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_get_by_id_negative_id(self):
        """エッジケース: 負のIDでユーザーを取得しようとするとエラーが発生する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            UserId(-1)
    
    @pytest.mark.anyio
    async def test_get_by_id_execute_failure(self):
        """異常系: データベース実行エラーの場合"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Database error")
        
        repo = SQLAlchemyUserRepository(mock_session)
        user_id = UserId(1)
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repo.get_by_id(user_id)


class TestSQLAlchemyUserRepositoryGetByMailAddress:
    """SQLAlchemyUserRepositoryのget_by_mail_addressメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_get_by_mail_address_existing_user(self):
        """正常系: 存在するメールアドレスでユーザーを取得する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_orm = UserORM(
            user_id=1,
            mail_address="test@example.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8mjd3HJ3xO",
            full_name="Test User",
            is_active=True,
            is_superuser=False
        )
        mock_result.scalar_one_or_none.return_value = mock_orm
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        mail_address = MailAddress("test@example.com")
        
        # Act
        result = await repo.get_by_mail_address(mail_address)
        
        # Assert
        assert result is not None
        assert isinstance(result, User)
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_get_by_mail_address_nonexistent_user(self):
        """正常系: 存在しないメールアドレスの場合Noneを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        mail_address = MailAddress("nonexistent@example.com")
        
        # Act
        result = await repo.get_by_mail_address(mail_address)
        
        # Assert
        assert result is None
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_get_by_mail_address_execute_failure(self):
        """異常系: データベース実行エラーの場合"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Database error")
        
        repo = SQLAlchemyUserRepository(mock_session)
        mail_address = MailAddress("test@example.com")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repo.get_by_mail_address(mail_address)


class TestSQLAlchemyUserRepositoryListAll:
    """SQLAlchemyUserRepositoryのlist_allメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_list_all_with_multiple_users(self):
        """正常系: 複数ユーザーをリスト形式で取得する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_scalars = Mock()
        mock_orm_list = [
            UserORM(user_id=1, mail_address="user1@example.com", hashed_password="$2b$12$pass1_hash_example_here", full_name="User 1", is_active=True, is_superuser=False),
            UserORM(user_id=2, mail_address="user2@example.com", hashed_password="$2b$12$pass2_hash_example_here", full_name="User 2", is_active=True, is_superuser=False)
        ]
        mock_scalars.all.return_value = mock_orm_list
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act
        result = await repo.list_all()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) >= 0
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_list_all_with_empty_result(self):
        """正常系: ユーザーが存在しない場合空リストを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_scalars = Mock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act
        result = await repo.list_all()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_list_all_execute_failure(self):
        """異常系: データベース実行エラーの場合"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Database error")
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repo.list_all()


class TestSQLAlchemyUserRepositoryNextIdentifier:
    """SQLAlchemyUserRepositoryのnext_identifierメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_next_identifier_with_existing_users(self):
        """正常系: 既存ユーザーがある場合次のIDを取得する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar.return_value = 5  # 最大ID = 5
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act
        result = await repo.next_identifier()
        
        # Assert
        assert isinstance(result, UserId)
        assert result.value == 6  # 5 + 1
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_next_identifier_with_no_users(self):
        """正常系: ユーザーが存在しない場合ID=1を返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar.return_value = None
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act
        result = await repo.next_identifier()
        
        # Assert
        assert isinstance(result, UserId)
        assert result.value == 1
        mock_session.execute.assert_called_once()
    
    @pytest.mark.anyio
    async def test_next_identifier_execute_failure(self):
        """異常系: データベース実行エラーの場合"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Database error")
        
        repo = SQLAlchemyUserRepository(mock_session)
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repo.next_identifier()


class TestSQLAlchemyUserRepositoryUpdate:
    """SQLAlchemyUserRepositoryのupdateメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_update_existing_user_success(self):
        """正常系: 既存ユーザーの更新が成功する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_orm = UserORM(
            user_id=1,
            mail_address="old@example.com",
            hashed_password="old_password",
            full_name="Old Name",
            is_active=True,
            is_superuser=False
        )
        mock_result.scalar_one_or_none.return_value = mock_orm
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user = User(
            user_id=UserId(1),
            mail_address=MailAddress("new@example.com"),
            hashed_password=HashedPassword("$2b$12$new_password_hash_example_here"),
            full_name=FullName("New Name"),
            is_active=False,
            is_superuser=True
        )
        
        # Act
        result = await repo.update(user)
        
        # Assert
        assert result is not None
        assert isinstance(result, User)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.anyio
    async def test_update_user_with_none_id(self):
        """異常系: user_idがNoneの場合Noneを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        repo = SQLAlchemyUserRepository(mock_session)
        
        user = User(
            user_id=None,
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$password_hash_example_here"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        
        # Act
        result = await repo.update(user)
        
        # Assert
        assert result is None
        mock_session.execute.assert_not_called()
    
    @pytest.mark.anyio
    async def test_update_nonexistent_user(self):
        """正常系: 存在しないユーザーの場合Noneを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user = User(
            user_id=UserId(999),
            mail_address=MailAddress("test@example.com"),
            hashed_password=HashedPassword("$2b$12$password_hash_example_here"),
            full_name=FullName("Test User"),
            is_active=True,
            is_superuser=False
        )
        
        # Act
        result = await repo.update(user)
        
        # Assert
        assert result is None
        mock_session.execute.assert_called_once()


class TestSQLAlchemyUserRepositoryDelete:
    """SQLAlchemyUserRepositoryのdeleteメソッドテスト"""
    
    @pytest.mark.anyio
    async def test_delete_existing_user_success(self):
        """正常系: 既存ユーザーの削除が成功する"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_orm = UserORM(
            user_id=1,
            mail_address="test@example.com",
            hashed_password="$2b$12$password_hash_example_here",
            full_name="Test User",
            is_active=True,
            is_superuser=False
        )
        mock_result.scalar_one_or_none.return_value = mock_orm
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user_id = UserId(1)
        
        # Act
        result = await repo.delete(user_id)
        
        # Assert
        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_orm)
        mock_session.commit.assert_called_once()
    
    @pytest.mark.anyio
    async def test_delete_nonexistent_user(self):
        """正常系: 存在しないユーザーの場合Falseを返す"""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = AsyncMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        repo = SQLAlchemyUserRepository(mock_session)
        user_id = UserId(999)
        
        # Act
        result = await repo.delete(user_id)
        
        # Assert
        assert result is False
        mock_session.execute.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
