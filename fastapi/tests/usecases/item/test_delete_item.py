"""
delete_item.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.item.delete_item import DeleteItemUseCase
from app.repository.item_repository import ItemRepository


class TestDeleteItemUseCase:
    """DeleteItemUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでDeleteItemUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=ItemRepository)

        # Act
        use_case = DeleteItemUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_deletes_item_successfully(self):
        """正常系: アイテムを正常に削除する"""
        # Arrange
        item_id = 1
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.delete.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してアイテムを削除する"""
        # Arrange
        item_id = 0
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.delete.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_negative_id(self):
        """エッジケース: 負のIDを指定してアイテムを削除する"""
        # Arrange
        item_id = -1
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.delete.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_with_large_id(self):
        """エッジケース: 大きなIDを指定してアイテムを削除する"""
        # Arrange
        item_id = 999999999
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.delete.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_always_returns_none(self):
        """正常系: 削除処理は常にNoneを返す"""
        # Arrange
        item_id = 123
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id)

        # Assert
        assert result is None
        mock_repo.delete.assert_called_once_with(item_id)

    @pytest.mark.anyio
    async def test_execute_calls_repository_delete_method(self):
        """正常系: リポジトリのdeleteメソッドが正しく呼ばれることを確認"""
        # Arrange
        item_id = 456
        
        mock_repo = AsyncMock(spec=ItemRepository)
        mock_repo.delete.return_value = None
        
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        await use_case.execute(item_id)

        # Assert
        mock_repo.delete.assert_called_once_with(item_id)
        # 他のリポジトリメソッドは呼ばれないことを確認
        mock_repo.save.assert_not_called()
        mock_repo.get_by_id.assert_not_called()
        mock_repo.list_all.assert_not_called()
        mock_repo.update.assert_not_called()
        mock_repo.next_identifier.assert_not_called()
