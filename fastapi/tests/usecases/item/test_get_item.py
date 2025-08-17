"""
get_item.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.get_item import GetItemUseCase
from app.domain.items import Item
from app.repository.item_repository import ItemRepository


class TestGetItemUseCase:
    """GetItemUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでGetItemUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = GetItemUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_returns_existing_item(self):
        """正常系: 存在するアイテムを取得する"""
        # Arrange
        item_id = 1
        expected_item = Item(item_id=item_id, name="テストアイテム", category_ids=[1, 2, 3])
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result == expected_item
        assert result is not None
        assert result.id == item_id
        assert result.name == "テストアイテム"
        assert result.category_ids == [1, 2, 3]
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_returns_none_for_nonexistent_item(self):
        """正常系: 存在しないアイテムの場合Noneを返す"""
        # Arrange
        item_id = 999
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_item_having_no_categories(self):
        """正常系: カテゴリを持たないアイテムを取得する"""
        # Arrange
        item_id = 2
        expected_item = Item(item_id=item_id, name="カテゴリなしアイテム", category_ids=None)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result == expected_item
        assert result is not None
        assert result.id == item_id
        assert result.name == "カテゴリなしアイテム"
        assert result.category_ids is None
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_item_having_empty_categories(self):
        """正常系: 空のカテゴリリストを持つアイテムを取得する"""
        # Arrange
        item_id = 3
        expected_item = Item(item_id=item_id, name="空カテゴリアイテム", category_ids=[])
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result == expected_item
        assert result is not None
        assert result.id == item_id
        assert result.name == "空カテゴリアイテム"
        assert result.category_ids == []
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してアイテムを取得する"""
        # Arrange
        item_id = 0
        expected_item = Item(item_id=item_id, name="IDが0のアイテム", category_ids=[1])
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result == expected_item
        assert result is not None
        assert result.id == 0
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_negative_id(self):
        """エッジケース: 負のIDを指定してアイテムを取得する"""
        # Arrange
        item_id = -1
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_large_id(self):
        """エッジケース: 大きなIDを指定してアイテムを取得する"""
        # Arrange
        item_id = 999999999
        expected_item = Item(item_id=item_id, name="大きなIDのアイテム", category_ids=[1, 2])
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result == expected_item
        assert result is not None
        assert result.id == item_id
        mock_repo.get_by_id.assert_called_once_with(item_id)
