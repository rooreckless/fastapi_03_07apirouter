"""
update_item_name.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.update_item_name import UpdateItemNameUseCase
from app.domain.items import Item
from app.repository.item_repository import ItemRepository


class TestUpdateItemNameUseCase:
    """UpdateItemNameUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでUpdateItemNameUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = UpdateItemNameUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_updates_existing_item_name_successfully(self):
        """正常系: 存在するアイテムの名前を正常に更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2, 3]
        new_name = "更新されたアイテム名"
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert isinstance(result, Item)
        assert result.id == item_id
        assert result.name == new_name
        assert result.category_ids == original_category_ids  # カテゴリIDは変更されない
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_raises_error_for_nonexistent_item(self):
        """異常系: 存在しないアイテムの場合ValueErrorが発生する"""
        # Arrange
        item_id = 999
        new_name = "更新されたアイテム名"
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Item not found"):
            await use_case.execute(item_id, new_name)
        
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_not_called()

    @pytest.mark.anyio
    async def test_execute_with_empty_name(self):
        """エッジケース: 空の名前でアイテム名を更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = ""
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result.name == ""
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_same_name(self):
        """エッジケース: 同じ名前でアイテム名を更新する"""
        # Arrange
        item_id = 1
        same_name = "同じアイテム名"
        original_category_ids = [1, 2, 3]
        
        existing_item = Item(item_id=item_id, name=same_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, same_name)

        # Assert
        assert result.name == same_name
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_long_name(self):
        """エッジケース: 長い名前でアイテム名を更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1]
        new_name = "a" * 1000  # 1000文字の長い名前
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result.name == new_name
        assert len(result.name) == 1000
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_special_characters_name(self):
        """エッジケース: 特殊文字を含む名前でアイテム名を更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result.name == new_name
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_unicode_name(self):
        """エッジケース: Unicode文字を含む名前でアイテム名を更新する"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2, 3]
        new_name = "テスト🐶🐱🎉アイテム"
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result.name == new_name
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してアイテム名を更新する"""
        # Arrange
        item_id = 0
        original_name = "元のアイテム名"
        original_category_ids = [1, 2]
        new_name = "更新されたアイテム名"
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result.id == 0
        assert result.name == new_name
        assert result.category_ids == original_category_ids
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_with_negative_id_raises_error(self):
        """異常系: 負のIDを指定した場合、存在しないのでValueErrorが発生する"""
        # Arrange
        item_id = -1
        new_name = "更新されたアイテム名"
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Item not found"):
            await use_case.execute(item_id, new_name)
        
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_not_called()

    @pytest.mark.anyio
    async def test_execute_modifies_item_object_directly(self):
        """正常系: アイテムオブジェクトが直接変更されることを確認"""
        # Arrange
        item_id = 1
        original_name = "元のアイテム名"
        original_category_ids = [1, 2, 3]
        new_name = "更新されたアイテム名"
        
        existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
        original_item_ref = existing_item
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.get_by_id.return_value = existing_item
        mock_repo.update.return_value = None
        
        use_case = UpdateItemNameUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id, new_name)

        # Assert
        assert result is original_item_ref  # 同じオブジェクトインスタンス
        assert existing_item.name == new_name  # 元のオブジェクトも変更されている
        assert existing_item.category_ids == original_category_ids  # カテゴリIDは変更されない
        mock_repo.get_by_id.assert_called_once_with(item_id)
        mock_repo.update.assert_called_once_with(existing_item)

    @pytest.mark.anyio
    async def test_execute_preserves_category_ids_regardless_of_value(self):
        """正常系: 名前のみ更新され、カテゴリIDは様々な値でも保持される"""
        # Arrange
        test_cases = [
            [1, 2, 3],
            [],
            None,
            [0, -1, 999999]
        ]
        
        for i, original_category_ids in enumerate(test_cases):
            item_id = i + 1
            original_name = f"元のアイテム名{i}"
            new_name = f"更新されたアイテム名{i}"
            
            existing_item = Item(item_id=item_id, name=original_name, category_ids=original_category_ids)
            
            mock_repo = AsyncMock(spec=ItemRepository)
            mock_repo.get_by_id.return_value = existing_item
            mock_repo.update.return_value = None
            
            use_case = UpdateItemNameUseCase(mock_repo)

            # Act
            result = await use_case.execute(item_id, new_name)

            # Assert
            assert result.name == new_name
            assert result.category_ids == original_category_ids
            mock_repo.get_by_id.assert_called_with(item_id)
            mock_repo.update.assert_called_with(existing_item)
