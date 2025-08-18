"""
create_item.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.create_item import CreateItemUseCase
from app.domain.items import Item
from app.repository.item_repository import ItemRepository


class TestCreateItemUseCase:
    """CreateItemUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでCreateItemUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = CreateItemUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_creates_item_successfully(self):
        """正常系: アイテムを正常に作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 1
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [1, 2, 3]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 1
        assert result.name == item_name
        assert result.category_ids == category_ids
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()
        
        # saveに渡されたアイテムを検証
        saved_item = mock_repo.save.call_args[0][0]
        assert saved_item.id == 1
        assert saved_item.name == item_name
        assert saved_item.category_ids == category_ids

    @pytest.mark.anyio
    async def test_execute_with_empty_category_ids(self):
        """正常系: 空のカテゴリIDリストでアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 2
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = []

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 2
        assert result.name == item_name
        assert result.category_ids == []
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_single_category_id(self):
        """正常系: 単一のカテゴリIDでアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 3
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [5]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 3
        assert result.name == item_name
        assert result.category_ids == [5]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_empty_name(self):
        """エッジケース: 空の名前でアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 4
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = ""
        category_ids = [1, 2]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 4
        assert result.name == ""
        assert result.category_ids == [1, 2]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_long_name(self):
        """エッジケース: 長い名前でアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 5
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "a" * 1000  # 1000文字の長い名前
        category_ids = [1]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 5
        assert result.name == item_name
        assert result.name is not None
        assert len(result.name) == 1000
        assert result.category_ids == [1]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_many_category_ids(self):
        """エッジケース: 多数のカテゴリIDでアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 6
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = list(range(1, 101))  # 1から100までのカテゴリID

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 6
        assert result.name == item_name
        assert result.category_ids == category_ids
        assert result.category_ids is not None
        assert len(result.category_ids) == 100
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_duplicate_category_ids(self):
        """エッジケース: 重複するカテゴリIDでアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 7
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [1, 2, 1, 3, 2]  # 重複あり

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 7
        assert result.name == item_name
        assert result.category_ids == [1, 2, 1, 3, 2]  # 重複を保持
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_zero_category_ids(self):
        """エッジケース: カテゴリIDに0を含むアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 8
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [0, 1, 2]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 8
        assert result.name == item_name
        assert result.category_ids == [0, 1, 2]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_negative_category_ids(self):
        """エッジケース: 負のカテゴリIDでアイテムを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 9
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [-1, -2, 1]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 9
        assert result.name == item_name
        assert result.category_ids == [-1, -2, 1]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_zero_id_from_repository(self):
        """エッジケース: リポジトリから0のIDが返される場合"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.next_identifier.return_value = 0
        mock_repo.save.return_value = None
        
        use_case = CreateItemUseCase(mock_repo)
        item_name = "テストアイテム"
        category_ids = [1, 2]

        # Act
        result = await use_case.execute(item_name, category_ids)

        # Assert
        assert isinstance(result, Item)
        assert result.id == 0
        assert result.name == item_name
        assert result.category_ids == [1, 2]
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()
