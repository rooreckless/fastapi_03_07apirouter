"""
update_category.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.category.update_category import UpdateCategoryUseCase
from app.domain.category import Category
from app.repository.category_repository import CategoryRepository


class TestUpdateCategoryUseCase:
    """UpdateCategoryUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでUpdateCategoryUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)

        # Act
        use_case = UpdateCategoryUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_updates_existing_category_successfully(self):
        """正常系: 存在するカテゴリを正常に更新する"""
        # Arrange
        category_id = 1
        original_name = "元のカテゴリ名"
        new_name = "更新されたカテゴリ名"
        
        existing_category = Category(category_id=category_id, name=original_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is not None
        assert isinstance(result, Category)
        assert result.id == category_id
        assert result.name == new_name
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_returns_none_for_nonexistent_category(self):
        """正常系: 存在しないカテゴリの場合Noneを返す"""
        # Arrange
        category_id = 999
        new_name = "更新されたカテゴリ名"
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_not_called()

    @pytest.mark.anyio
    async def test_execute_with_empty_name(self):
        """エッジケース: 空の名前でカテゴリを更新する"""
        # Arrange
        category_id = 1
        original_name = "元のカテゴリ名"
        new_name = ""
        
        existing_category = Category(category_id=category_id, name=original_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is not None
        assert result.name == ""
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_with_same_name(self):
        """エッジケース: 同じ名前でカテゴリを更新する"""
        # Arrange
        category_id = 1
        same_name = "同じカテゴリ名"
        
        existing_category = Category(category_id=category_id, name=same_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, same_name)

        # Assert
        assert result is not None
        assert result.name == same_name
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_with_long_name(self):
        """エッジケース: 長い名前でカテゴリを更新する"""
        # Arrange
        category_id = 1
        original_name = "元のカテゴリ名"
        new_name = "a" * 1000  # 1000文字の長い名前
        
        existing_category = Category(category_id=category_id, name=original_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is not None
        assert result.name == new_name
        assert len(result.name) == 1000
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_with_special_characters_name(self):
        """エッジケース: 特殊文字を含む名前でカテゴリを更新する"""
        # Arrange
        category_id = 1
        original_name = "元のカテゴリ名"
        new_name = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"
        
        existing_category = Category(category_id=category_id, name=original_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is not None
        assert result.name == new_name
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してカテゴリを更新する"""
        # Arrange
        category_id = 0
        original_name = "元のカテゴリ名"
        new_name = "更新されたカテゴリ名"
        
        existing_category = Category(category_id=category_id, name=original_name)
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is not None
        assert result.id == 0
        assert result.name == new_name
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)

    @pytest.mark.anyio
    async def test_execute_with_negative_id(self):
        """エッジケース: 負のIDを指定してカテゴリを更新する"""
        # Arrange
        category_id = -1
        new_name = "更新されたカテゴリ名"
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_not_called()

    @pytest.mark.anyio
    async def test_execute_modifies_category_object_directly(self):
        """正常系: カテゴリオブジェクトが直接変更されることを確認"""
        # Arrange
        category_id = 1
        original_name = "元のカテゴリ名"
        new_name = "更新されたカテゴリ名"
        
        existing_category = Category(category_id=category_id, name=original_name)
        original_category_ref = existing_category
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = existing_category
        mock_repo.update.return_value = None
        
        use_case = UpdateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id, new_name)

        # Assert
        assert result is original_category_ref  # 同じオブジェクトインスタンス
        assert existing_category.name == new_name  # 元のオブジェクトも変更されている
        mock_repo.get_by_id.assert_called_once_with(category_id)
        mock_repo.update.assert_called_once_with(existing_category)
