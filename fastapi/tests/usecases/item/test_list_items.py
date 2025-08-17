"""
list_items.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.list_items import ListItemsUseCase
from app.domain.items import Item
from app.repository.item_repository import ItemRepository


class TestListItemsUseCase:
    """ListItemsUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでListItemsUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = ListItemsUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_returns_multiple_items(self):
        """正常系: 複数のアイテムを取得する"""
        # Arrange
        expected_items = [
            Item(item_id=1, name="アイテム1", category_ids=[1, 2]),
            Item(item_id=2, name="アイテム2", category_ids=[3]),
            Item(item_id=3, name="アイテム3", category_ids=None)
        ]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert len(result) == 3
        assert all(isinstance(item, Item) for item in result)
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_empty_list(self):
        """正常系: アイテムが存在しない場合は空のリストを返す"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = []
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == []
        assert len(result) == 0
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_single_item(self):
        """エッジケース: 単一のアイテムを取得する"""
        # Arrange
        expected_items = [Item(item_id=1, name="唯一のアイテム", category_ids=[1, 2, 3])]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "唯一のアイテム"
        assert result[0].category_ids == [1, 2, 3]
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_items_with_various_category_configurations(self):
        """正常系: 様々なカテゴリ設定を持つアイテムを取得する"""
        # Arrange
        expected_items = [
            Item(item_id=1, name="カテゴリありアイテム", category_ids=[1, 2, 3]),
            Item(item_id=2, name="カテゴリなしアイテム", category_ids=None),
            Item(item_id=3, name="空カテゴリアイテム", category_ids=[]),
            Item(item_id=4, name="単一カテゴリアイテム", category_ids=[5])
        ]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert len(result) == 4
        assert result[0].category_ids == [1, 2, 3]
        assert result[1].category_ids is None
        assert result[2].category_ids == []
        assert result[3].category_ids == [5]
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_many_items(self):
        """エッジケース: 大量のアイテムを取得する"""
        # Arrange
        expected_items = [
            Item(item_id=i, name=f"アイテム{i}", category_ids=[i % 3 + 1])
            for i in range(1, 1001)  # 1000個のアイテム
        ]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert len(result) == 1000
        assert all(isinstance(item, Item) for item in result)
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_preserves_item_order(self):
        """正常系: アイテムの順序が保持される"""
        # Arrange
        expected_items = [
            Item(item_id=5, name="5番目", category_ids=[5]),
            Item(item_id=1, name="1番目", category_ids=[1]),
            Item(item_id=3, name="3番目", category_ids=[3]),
            Item(item_id=2, name="2番目", category_ids=[2])
        ]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert result[0].id == 5
        assert result[1].id == 1
        assert result[2].id == 3
        assert result[3].id == 2
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_items_having_zero_or_negative_ids(self):
        """エッジケース: 0や負のIDを持つアイテムを含むリストを取得する"""
        # Arrange
        expected_items = [
            Item(item_id=0, name="IDが0のアイテム", category_ids=[1]),
            Item(item_id=-1, name="負のIDのアイテム", category_ids=[2]),
            Item(item_id=1, name="正のIDのアイテム", category_ids=[3])
        ]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.list_all.return_value = expected_items
        
        use_case = ListItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_items
        assert len(result) == 3
        assert result[0].id == 0
        assert result[1].id == -1
        assert result[2].id == 1
        mock_repo.list_all.assert_called_once()
