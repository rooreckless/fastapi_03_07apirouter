"""
update_item.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.update_item import UpdateItemUseCase
from app.domain.items import Item
from app.repository.item_repository import ItemRepository


class TestUpdateItemUseCase:
    """UpdateItemUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでUpdateItemUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = UpdateItemUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_updates_existing_item_successfully(self):
        """正常系: 存在するアイテムを正常に更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "更新されたアイテム名"
        new_category_ids = [3, 4, 5]
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert isinstance(result, Item)
        assert result.id == item_id
        assert result.name == new_name
        assert result.category_ids == new_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_returns_none_for_nonexistent_item(self):
        """正常系: 存在しないアイテムの場合Noneを返す"""
        # Arrange
        item_id = 999
        new_name = "更新されたアイテム名"
        new_category_ids = [1, 2, 3]
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_not_called()

    @pytest.mark.anyio
    async def test_execute_with_none_category_ids(self):
        """正常系: category_idsをNoneで更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2, 3]
        new_name = "更新されたアイテム名"
        new_category_ids = None
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.name == new_name
        assert result.category_ids is None
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_empty_category_ids(self):
        """正常系: category_idsを空のリストで更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2, 3]
        new_name = "更新されたアイテム名"
        new_category_ids = []
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.name == new_name
        assert result.category_ids == []
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_empty_name(self):
        """エッジケース: 空の名前でアイテムを更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = ""
        new_category_ids = [3, 4]
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.name == ""
        assert result.category_ids == [3, 4]
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_same_values(self):
        """エッジケース: 同じ値でアイテムを更新する"""
        # Arrange
        item_id = 1
        same_name = "同じアイテム名"
        same_category_ids = [1, 2, 3]
        
        existing_item = Item(item_id=item_id, name=same_name, category_ids=same_category_ids.copy())
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, same_name, same_category_ids)

        # Assert
        assert result is not None
        assert result.name == same_name
        assert result.category_ids == same_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_long_name(self):
        """エッジケース: 長い名前でアイテムを更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1]
        new_name = "a" * 1000  # 1000文字の長い名前
        new_category_ids = [2, 3]
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.name == new_name
        assert len(result.name) == 1000
        assert result.category_ids == [2, 3]
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_many_category_ids(self):
        """エッジケース: 多数のカテゴリIDでアイテムを更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "更新されたアイテム名"
        new_category_ids = list(range(1, 101))  # 1から100までのカテゴリID
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.name == new_name
        assert result.category_ids == new_category_ids
        assert result.category_ids is not None
        assert len(result.category_ids) == 100
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してアイテムを更新する"""
        # Arrange
        item_id = 0
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "更新されたアイテム名"
        new_category_ids = [3, 4]
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is not None
        assert result.id == 0
        assert result.name == new_name
        assert result.category_ids == [3, 4]
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_modifies_item_object_directly(self):
        """正常系: アイテムオブジェクトが直接変更されることを確認"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "更新されたアイテム名"
        new_category_ids = [3, 4, 5]
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        original_item_ref = existing_item
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name, new_category_ids)

        # Assert
        assert result is original_item_ref  # 同じオブジェクトインスタンス
        assert existing_item.name == new_name  # 元のオブジェクトも変更されている
        assert existing_item.category_ids == new_category_ids  # 元のオブジェクトも変更されている
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)
