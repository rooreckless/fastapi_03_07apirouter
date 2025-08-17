"""
Tests for SQLAlchemyItemRepository class.

This module contains unit tests for the SQLAlchemyItemRepository implementation
using pytest and pytest-mock, without unittest.mock.
Tests cover all methods: save, list_all, get_by_id, next_identifier, update, delete, and error scenarios.

AsyncSession のモック: データベースセッションの完全モック化
ORM モデルのモック: SQLAlchemyモデルの複雑な関係性をモック対応
"""

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.items.item import Item
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.repositories.item_repo_impl import SQLAlchemyItemRepository


class TestSQLAlchemyItemRepositoryInit:
    """Tests for SQLAlchemyItemRepository initialization."""

    def test_init_with_valid_session(self, mocker: MockerFixture) -> None:
        """Test initialization with valid AsyncSession."""
        mock_session = mocker.Mock(spec=AsyncSession)
        
        repository = SQLAlchemyItemRepository(mock_session)
        
        assert repository.db is mock_session

    def test_init_with_none_session(self) -> None:
        """Test initialization with None session."""
        repository = SQLAlchemyItemRepository(None)  # type: ignore[arg-type]
        assert repository.db is None


class TestSQLAlchemyItemRepositorySave:
    """Tests for save method."""

    @pytest.mark.anyio
    async def test_save_item_with_no_categories(self, mocker: MockerFixture) -> None:
        """Test saving item without categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=1, name="Test Item", category_ids=None)

        # Act
        await repository.save(item)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert isinstance(added_orm, ItemORM)
        assert added_orm.item_id == 1
        assert added_orm.item_name == "Test Item"
        assert added_orm.categories == []
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_with_empty_categories(self, mocker: MockerFixture) -> None:
        """Test saving item with empty category list."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=2, name="Empty Categories", category_ids=[])

        # Act
        await repository.save(item)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert added_orm.categories == []
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_with_categories(self, mocker: MockerFixture) -> None:
        """Test saving item with categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        
        # Mock category result
        mock_result = mocker.Mock()
        mock_categories = [
            mocker.Mock(category_id=1, category_name="Electronics"),
            mocker.Mock(category_id=2, category_name="Books"),
        ]
        mock_result.scalars.return_value.all.return_value = mock_categories
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        
        # Mock ItemORM constructor
        mock_item_orm = mocker.Mock()
        mocker.patch('app.infrastructure.sqlalchemy.repositories.item_repo_impl.ItemORM', return_value=mock_item_orm)
        
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=3, name="Item with Categories", category_ids=[1, 2])

        # Act
        await repository.save(item)

        # Assert
        mock_session.execute.assert_called_once()
        mock_session.add.assert_called_once_with(mock_item_orm)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_with_single_category(self, mocker: MockerFixture) -> None:
        """Test saving item with single category."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        
        mock_result = mocker.Mock()
        mock_category = mocker.Mock(category_id=5, category_name="Sports")
        mock_result.scalars.return_value.all.return_value = [mock_category]
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        
        # Mock ItemORM constructor
        mock_item_orm = mocker.Mock()
        mocker.patch('app.infrastructure.sqlalchemy.repositories.item_repo_impl.ItemORM', return_value=mock_item_orm)
        
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=4, name="Sports Item", category_ids=[5])

        # Act
        await repository.save(item)

        # Assert
        mock_session.execute.assert_called_once()
        mock_session.add.assert_called_once_with(mock_item_orm)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_with_japanese_name(self, mocker: MockerFixture) -> None:
        """Test saving item with Japanese name."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=6, name="日本語商品", category_ids=None)

        # Act
        await repository.save(item)

        # Assert
        mock_session.add.assert_called_once()
        added_orm = mock_session.add.call_args[0][0]
        assert added_orm.item_name == "日本語商品"
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_commit_failure(self, mocker: MockerFixture) -> None:
        """Test save method when commit fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.add = mocker.Mock()
        mock_session.commit = mocker.AsyncMock(side_effect=Exception("Database error"))
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=7, name="Fail Item", category_ids=None)

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await repository.save(item)
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_save_item_category_execute_failure(self, mocker: MockerFixture) -> None:
        """Test save method when category execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Category query error"))
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=8, name="Category Fail", category_ids=[1])

        # Act & Assert
        with pytest.raises(Exception, match="Category query error"):
            await repository.save(item)
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyItemRepositoryListAll:
    """Tests for list_all method."""

    @pytest.mark.anyio
    async def test_list_all_with_multiple_items(self, mocker: MockerFixture) -> None:
        """Test listing all items when multiple exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        
        # Create mock ORM items with categories
        mock_category1 = mocker.Mock(category_id=1, category_name="Electronics")
        mock_category2 = mocker.Mock(category_id=2, category_name="Books")
        
        mock_item1 = mocker.Mock(item_id=1, item_name="Laptop")
        mock_item1.categories = [mock_category1]
        
        mock_item2 = mocker.Mock(item_id=2, item_name="Novel")
        mock_item2.categories = [mock_category2]
        
        mock_item3 = mocker.Mock(item_id=3, item_name="Generic Item")
        mock_item3.categories = []
        
        mock_result.scalars.return_value.all.return_value = [mock_item1, mock_item2, mock_item3]
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        items = await repository.list_all()

        # Assert
        assert len(items) == 3
        assert items[0].id == 1
        assert items[0].name == "Laptop"
        assert items[0].category_ids == [1]
        assert items[1].id == 2
        assert items[1].name == "Novel"
        assert items[1].category_ids == [2]
        assert items[2].id == 3
        assert items[2].name == "Generic Item"
        assert items[2].category_ids == []
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_with_empty_result(self, mocker: MockerFixture) -> None:
        """Test listing all items when none exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        items = await repository.list_all()

        # Assert
        assert items == []
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_with_multi_category_item(self, mocker: MockerFixture) -> None:
        """Test listing items with multiple categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        
        mock_category1 = mocker.Mock(category_id=1, category_name="Electronics")
        mock_category2 = mocker.Mock(category_id=2, category_name="Gaming")
        mock_category3 = mocker.Mock(category_id=3, category_name="Accessories")
        
        mock_item = mocker.Mock(item_id=10, item_name="Gaming Laptop")
        mock_item.categories = [mock_category1, mock_category2, mock_category3]
        
        mock_result.scalars.return_value.all.return_value = [mock_item]
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        items = await repository.list_all()

        # Assert
        assert len(items) == 1
        assert items[0].id == 10
        assert items[0].name == "Gaming Laptop"
        assert set(items[0].category_ids) == {1, 2, 3}
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_list_all_execute_failure(self, mocker: MockerFixture) -> None:
        """Test list_all method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.list_all()
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyItemRepositoryGetById:
    """Tests for get_by_id method."""

    @pytest.mark.anyio
    async def test_get_by_id_existing_item_with_categories(self, mocker: MockerFixture) -> None:
        """Test getting existing item with categories by ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        
        mock_category1 = mocker.Mock(category_id=5, category_name="Food")
        mock_category2 = mocker.Mock(category_id=6, category_name="Organic")
        
        mock_item = mocker.Mock(item_id=20, item_name="Organic Apple")
        mock_item.categories = [mock_category1, mock_category2]
        
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        item = await repository.get_by_id(20)

        # Assert
        assert item is not None
        assert item.id == 20
        assert item.name == "Organic Apple"
        assert set(item.category_ids) == {5, 6}
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_existing_item_no_categories(self, mocker: MockerFixture) -> None:
        """Test getting existing item without categories by ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        
        mock_item = mocker.Mock(item_id=21, item_name="Plain Item")
        mock_item.categories = []
        
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        item = await repository.get_by_id(21)

        # Assert
        assert item is not None
        assert item.id == 21
        assert item.name == "Plain Item"
        assert item.category_ids == []
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_nonexistent_item(self, mocker: MockerFixture) -> None:
        """Test getting nonexistent item by ID returns None."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        item = await repository.get_by_id(999)

        # Assert
        assert item is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_zero_id(self, mocker: MockerFixture) -> None:
        """Test getting item with ID 0."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        item = await repository.get_by_id(0)

        # Assert
        assert item is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_negative_id(self, mocker: MockerFixture) -> None:
        """Test getting item with negative ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        item = await repository.get_by_id(-1)

        # Assert
        assert item is None
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id_execute_failure(self, mocker: MockerFixture) -> None:
        """Test get_by_id method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.get_by_id(1)
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyItemRepositoryNextIdentifier:
    """Tests for next_identifier method."""

    @pytest.mark.anyio
    async def test_next_identifier_with_existing_items(self, mocker: MockerFixture) -> None:
        """Test next_identifier when items exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = 15
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 16
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_with_no_items(self, mocker: MockerFixture) -> None:
        """Test next_identifier when no items exist."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        repository = SQLAlchemyItemRepository(mock_session)

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
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        next_id = await repository.next_identifier()

        # Assert
        assert next_id == 1
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_next_identifier_execute_failure(self, mocker: MockerFixture) -> None:
        """Test next_identifier method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.next_identifier()
        
        mock_session.execute.assert_called_once()


class TestSQLAlchemyItemRepositoryUpdate:
    """Tests for update method."""

    @pytest.mark.anyio
    async def test_update_existing_item_name_only(self, mocker: MockerFixture) -> None:
        """Test successful update of existing item name only."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_item = mocker.Mock(item_id=30, item_name="Old Name")
        mock_item.categories = []
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=30, name="New Name", category_ids=None)

        # Act
        await repository.update(item)

        # Assert
        assert mock_item.item_name == "New Name"
        assert mock_item.categories == []
        assert item.category_ids == []
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_item_with_new_categories(self, mocker: MockerFixture) -> None:
        """Test update item with new categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        
        # Mock item query result
        mock_item_result = mocker.Mock()
        mock_item = mocker.Mock(item_id=31, item_name="Item")
        mock_item.categories = []
        mock_item_result.scalar_one_or_none.return_value = mock_item
        
        # Mock category query result
        mock_category_result = mocker.Mock()
        mock_categories = [
            mocker.Mock(category_id=10, category_name="Tech"),
            mocker.Mock(category_id=11, category_name="Gaming"),
        ]
        mock_category_result.scalars.return_value.all.return_value = mock_categories
        
        # Setup execute to return different results for different queries
        mock_session.execute = mocker.AsyncMock(side_effect=[mock_item_result, mock_category_result])
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=31, name="Updated Item", category_ids=[10, 11])

        # Act
        await repository.update(item)

        # Assert
        assert mock_item.item_name == "Updated Item"
        assert len(mock_item.categories) == 2
        assert mock_item.categories[0].category_id == 10
        assert mock_item.categories[1].category_id == 11
        assert set(item.category_ids) == {10, 11}
        assert mock_session.execute.call_count == 2
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_item_remove_all_categories(self, mocker: MockerFixture) -> None:
        """Test update item to remove all categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_item = mocker.Mock(item_id=32, item_name="Item with Categories")
        mock_old_category = mocker.Mock(category_id=20, category_name="Old")
        mock_item.categories = [mock_old_category]
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=32, name="Updated Item", category_ids=[])

        # Act
        await repository.update(item)

        # Assert
        assert mock_item.item_name == "Updated Item"
        assert mock_item.categories == []
        assert item.category_ids == []
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_item_with_none_categories(self, mocker: MockerFixture) -> None:
        """Test update item with None categories."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_item = mocker.Mock(item_id=33, item_name="Item")
        mock_old_category = mocker.Mock(category_id=25, category_name="Old")
        mock_item.categories = [mock_old_category]
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=33, name="Updated Item", category_ids=None)

        # Act
        await repository.update(item)

        # Assert
        assert mock_item.item_name == "Updated Item"
        assert mock_item.categories == []
        assert item.category_ids == []
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_update_nonexistent_item(self, mocker: MockerFixture) -> None:
        """Test update of nonexistent item does nothing."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=999, name="Nonexistent", category_ids=[1])

        # Act
        await repository.update(item)

        # Assert
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_not_called()

    @pytest.mark.anyio
    async def test_update_item_execute_failure(self, mocker: MockerFixture) -> None:
        """Test update method when execute fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.execute = mocker.AsyncMock(side_effect=Exception("Query error"))
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=1, name="Test", category_ids=None)

        # Act & Assert
        with pytest.raises(Exception, match="Query error"):
            await repository.update(item)
        
        mock_session.execute.assert_called_once()

    @pytest.mark.anyio
    async def test_update_item_commit_failure(self, mocker: MockerFixture) -> None:
        """Test update method when commit fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_result = mocker.Mock()
        mock_item = mocker.Mock(item_id=34, item_name="Old")
        mock_item.categories = []
        mock_result.scalar_one_or_none.return_value = mock_item
        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_session.commit = mocker.AsyncMock(side_effect=Exception("Commit error"))
        repository = SQLAlchemyItemRepository(mock_session)
        item = Item(item_id=34, name="New", category_ids=None)

        # Act & Assert
        with pytest.raises(Exception, match="Commit error"):
            await repository.update(item)
        
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()


class TestSQLAlchemyItemRepositoryDelete:
    """Tests for delete method."""

    @pytest.mark.anyio
    async def test_delete_existing_item_success(self, mocker: MockerFixture) -> None:
        """Test successful deletion of existing item."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_item = mocker.Mock(item_id=40, item_name="To Delete")
        mock_session.get = mocker.AsyncMock(return_value=mock_item)
        mock_session.delete = mocker.AsyncMock()
        mock_session.commit = mocker.AsyncMock()
        repository = SQLAlchemyItemRepository(mock_session)

        # Act
        await repository.delete(40)

        # Assert
        mock_session.get.assert_called_once_with(ItemORM, 40)
        mock_session.delete.assert_called_once_with(mock_item)
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_delete_nonexistent_item_raises_error(self, mocker: MockerFixture) -> None:
        """Test deletion of nonexistent item raises ValueError."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(return_value=None)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(ValueError, match="Item with ID 999 not found"):
            await repository.delete(999)
        
        mock_session.get.assert_called_once_with(ItemORM, 999)

    @pytest.mark.anyio
    async def test_delete_item_get_failure(self, mocker: MockerFixture) -> None:
        """Test delete method when get fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(side_effect=Exception("Get error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Get error"):
            await repository.delete(1)
        
        mock_session.get.assert_called_once()

    @pytest.mark.anyio
    async def test_delete_item_delete_failure(self, mocker: MockerFixture) -> None:
        """Test delete method when delete operation fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_item = mocker.Mock(item_id=41, item_name="Delete Fail")
        mock_session.get = mocker.AsyncMock(return_value=mock_item)
        mock_session.delete = mocker.AsyncMock(side_effect=Exception("Delete error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Delete error"):
            await repository.delete(41)
        
        mock_session.get.assert_called_once()
        mock_session.delete.assert_called_once()

    @pytest.mark.anyio
    async def test_delete_item_commit_failure(self, mocker: MockerFixture) -> None:
        """Test delete method when commit fails."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_item = mocker.Mock(item_id=42, item_name="Commit Fail")
        mock_session.get = mocker.AsyncMock(return_value=mock_item)
        mock_session.delete = mocker.AsyncMock()
        mock_session.commit = mocker.AsyncMock(side_effect=Exception("Commit error"))
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(Exception, match="Commit error"):
            await repository.delete(42)
        
        mock_session.get.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.anyio
    async def test_delete_item_zero_id(self, mocker: MockerFixture) -> None:
        """Test deletion with zero ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(return_value=None)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(ValueError, match="Item with ID 0 not found"):
            await repository.delete(0)
        
        mock_session.get.assert_called_once_with(ItemORM, 0)

    @pytest.mark.anyio
    async def test_delete_item_negative_id(self, mocker: MockerFixture) -> None:
        """Test deletion with negative ID."""
        # Arrange
        mock_session = mocker.Mock(spec=AsyncSession)
        mock_session.get = mocker.AsyncMock(return_value=None)
        repository = SQLAlchemyItemRepository(mock_session)

        # Act & Assert
        with pytest.raises(ValueError, match="Item with ID -1 not found"):
            await repository.delete(-1)
        
        mock_session.get.assert_called_once_with(ItemORM, -1)
