"""
Tests for SQLAlchemyCategoryRepository class.

This module contains unit tests for the SQLAlchemyCategoryRepository implementation
using pytest and pytest-mock, without unittest.mock.
Tests cover all methods: save, list_all, get_by_id, next_identifier, update, and error scenarios.

AsyncSession のモック: データベースセッションの完全モック化
ORM モデルのモック: SQLAlchemyモデルの複雑な関係性をモック対応
"""

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.category.category import Category
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.repositories.category_repo_impl import SQLAlchemyCategoryRepository


class TestSQLAlchemyCategoryRepositoryInit:
    """Tests for SQLAlchemyCategoryRepository initialization."""

    def test_init_with_valid_session(self, mocker: MockerFixture) -> None:
        """Test initialization with valid AsyncSession."""
        mock_session = mocker.Mock(spec=AsyncSession)
        
        repository = SQLAlchemyCategoryRepository(mock_session)
        
        assert repository.db is mock_session

    def test_init_with_none_session(self) -> None:
        """Test initialization with None session."""
        repository = SQLAlchemyCategoryRepository(None)  # type: ignore[arg-type]
        assert repository.db is None


class TestSQLAlchemyCategoryRepositorySave:
    """Tests for save method."""

    @pytest.mark.anyio
    async def test_save_new_category_success(self, mocker: MockerFixture) -> None:
        """Test successful saving of a new category."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=1, name="Electronics")

        # Act
        await repository.save(category)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert isinstance(added_orm, CategoryORM)
        assert added_orm.category_id == 1
        assert added_orm.category_name == "Electronics"
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_category_with_empty_name(self, mocker: MockerFixture) -> None:
        """Test saving category with empty name."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=2, name="")

        # Act
        await repository.save(category)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert added_orm.category_name == ""
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_category_with_japanese_name(self, mocker: MockerFixture) -> None:
        """Test saving category with Japanese name."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=3, name="家電製品")

        # Act
        await repository.save(category)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert added_orm.category_name == "家電製品"
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_category_commit_failure(self, mocker: MockerFixture) -> None:
        """Test save method when commit fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock(side_effect=Exception("Database error"))
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=4, name="Books")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repository.save(category)
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


class TestSQLAlchemyCategoryRepositoryListAll:
    """Tests for list_all method."""

    @pytest.mark.anyio
    async def test_list_all_with_multiple_categories(self, mocker: MockerFixture) -> None:
        """Test listing all categories when multiple exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        
        # Create mock objects instead of real ORM instances
        mock_orm_categories = [
            mocker.Mock(category_id=1, category_name="Electronics"),
            mocker.Mock(category_id=2, category_name="Books"),
            mocker.Mock(category_id=3, category_name="Clothing"),
        ]
        mock_result.scalars.return_value.all.return_value = mock_orm_categories
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        categories = await repository.list_all()

        # Assert
        assert len(categories) == 3
        assert categories[0].id == 1
        assert categories[0].name == "Electronics"
        assert categories[1].id == 2
        assert categories[1].name == "Books"
        assert categories[2].id == 3
        assert categories[2].name == "Clothing"
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_with_empty_result(self, mocker: MockerFixture) -> None:
        """Test listing all categories when none exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        categories = await repository.list_all()

        # Assert
        assert categories == []
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_with_single_category(self, mocker: MockerFixture) -> None:
        """Test listing all categories with single result."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_orm_category = mocker.Mock(category_id=5, category_name="Sports")
        mock_result.scalars.return_value.all.return_value = [mock_orm_category]
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        categories = await repository.list_all()

        # Assert
        assert len(categories) == 1
        assert categories[0].id == 5
        assert categories[0].name == "Sports"
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_execute_failure(self, mocker: MockerFixture) -> None:
        """Test list_all method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.list_all()
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyCategoryRepositoryGetById:
    """Tests for get_by_id method."""

    @pytest.mark.anyio
    async def test_get_by_id_existing_category(self, mocker: MockerFixture) -> None:
        """Test getting existing category by ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_orm_category = mocker.Mock(category_id=10, category_name="Technology")
        mock_result.scalar_one_or_none.return_value = mock_orm_category
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        category = await repository.get_by_id(10)

        # Assert
        assert category is not None
        assert category.id == 10
        assert category.name == "Technology"
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_nonexistent_category(self, mocker: MockerFixture) -> None:
        """Test getting nonexistent category by ID returns None."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        category = await repository.get_by_id(999)

        # Assert
        assert category is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_zero_id(self, mocker: MockerFixture) -> None:
        """Test getting category with ID 0."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        category = await repository.get_by_id(0)

        # Assert
        assert category is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_negative_id(self, mocker: MockerFixture) -> None:
        """Test getting category with negative ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        category = await repository.get_by_id(-1)

        # Assert
        assert category is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_execute_failure(self, mocker: MockerFixture) -> None:
        """Test get_by_id method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.get_by_id(1)
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyCategoryRepositoryNextIdentifier:
    """Tests for next_identifier method."""

    @pytest.mark.anyio
    async def test_next_identifier_with_existing_categories(self, mocker: MockerFixture) -> None:
        """Test next_identifier when categories exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = 5
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 6
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_with_no_categories(self, mocker: MockerFixture) -> None:
        """Test next_identifier when no categories exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 1
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_with_zero_max_id(self, mocker: MockerFixture) -> None:
        """Test next_identifier when max ID is 0."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = 0
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 1
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_with_large_max_id(self, mocker: MockerFixture) -> None:
        """Test next_identifier with large max ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = 999999
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 1000000
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_execute_failure(self, mocker: MockerFixture) -> None:
        """Test next_identifier method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyCategoryRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.next_identifier()
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyCategoryRepositoryUpdate:
    """Tests for update method."""

    @pytest.mark.anyio
    async def test_update_existing_category_success(self, mocker: MockerFixture) -> None:
        """Test successful update of existing category."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_orm_category = mocker.Mock(category_id=1, category_name="Old Name")
        mock_session.get = mocker.AsyncMock(return_value=mock_orm_category)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=1, name="New Name")

        # Act
        await repository.update(category)

        # Assert
        assert mock_orm_category.category_name == "New Name"
        mock_session.get.assert_called_once_with(CategoryORM, 1)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_nonexistent_category(self, mocker: MockerFixture) -> None:
        """Test update of nonexistent category does nothing."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(return_value=None)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=999, name="Nonexistent")

        # Act
        await repository.update(category)

        # Assert
        mock_session.get.assert_called_once_with(CategoryORM, 999)
        mock_session.commit.assert_not_called()

    @pytest.mark.anyio
    async def test_update_category_with_empty_name(self, mocker: MockerFixture) -> None:
        """Test update category with empty name."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_orm_category = mocker.Mock(category_id=2, category_name="Original")
        mock_session.get = mocker.AsyncMock(return_value=mock_orm_category)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=2, name="")

        # Act
        await repository.update(category)

        # Assert
        assert mock_orm_category.category_name == ""
        mock_session.get.assert_called_once_with(CategoryORM, 2)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_category_with_japanese_name(self, mocker: MockerFixture) -> None:
        """Test update category with Japanese name."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_orm_category = mocker.Mock(category_id=3, category_name="English")
        mock_session.get = mocker.AsyncMock(return_value=mock_orm_category)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=3, name="日本語名")

        # Act
        await repository.update(category)

        # Assert
        assert mock_orm_category.category_name == "日本語名"
        mock_session.get.assert_called_once_with(CategoryORM, 3)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_get_failure(self, mocker: MockerFixture) -> None:
        """Test update method when get fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=1, name="Test")

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.update(category)
        
        mock_session.get.assert_called_once()

    @pytest.mark.anyio
    async def test_update_commit_failure(self, mocker: MockerFixture) -> None:
        """Test update method when commit fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_orm_category = mocker.Mock(category_id=1, category_name="Old")
        mock_session.get = mocker.AsyncMock(return_value=mock_orm_category)
        mock_session.commit = mocker.AsyncMock(side_effect=Exception("Commit error"))
        repository = SQLAlchemyCategoryRepository(mock_session)
        category = Category(category_id=1, name="New")

        # Act & Assert
        with pytest.raises(Exception, match="Commit error"):
            await repository.update(category)
        
        mock_session.get.assert_called_once()
        mock_session.commit.assert_called_once()
