"""
get_category.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.category.get_category import GetCategoryUseCase
from app.domain.category import Category
from app.repository.category_repository import CategoryRepository


class TestGetCategoryUseCase:
    """GetCategoryUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでGetCategoryUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)

        # Act
        use_case = GetCategoryUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_returns_existing_category(self):
        """正常系: 存在するカテゴリを取得する"""
        # Arrange
        category_id = 1
        expected_category = Category(category_id=category_id, name="テストカテゴリ")
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = expected_category
        
        use_case = GetCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id)

        # Assert
        assert result == expected_category
        assert result is not None
        assert result.id == category_id
        assert result.name == "テストカテゴリ"
        mock_repo.get_by_id.assert_called_once_with(category_id)

    @pytest.mark.anyio
    async def test_execute_returns_none_for_nonexistent_category(self):
        """正常系: 存在しないカテゴリの場合Noneを返す"""
        # Arrange
        category_id = 999
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = GetCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(category_id)

    @pytest.mark.anyio
    async def test_execute_with_zero_id(self):
        """エッジケース: IDに0を指定してカテゴリを取得する"""
        # Arrange
        category_id = 0
        expected_category = Category(category_id=category_id, name="IDが0のカテゴリ")
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = expected_category
        
        use_case = GetCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id)

        # Assert
        assert result == expected_category
        assert result is not None
        assert result.id == 0
        mock_repo.get_by_id.assert_called_once_with(category_id)

    @pytest.mark.anyio
    async def test_execute_with_negative_id(self):
        """エッジケース: 負のIDを指定してカテゴリを取得する"""
        # Arrange
        category_id = -1
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = None
        
        use_case = GetCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(category_id)

    @pytest.mark.anyio
    async def test_execute_with_large_id(self):
        """エッジケース: 大きなIDを指定してカテゴリを取得する"""
        # Arrange
        category_id = 999999999
        expected_category = Category(category_id=category_id, name="大きなIDのカテゴリ")
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.get_by_id.return_value = expected_category
        
        use_case = GetCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_id)

        # Assert
        assert result == expected_category
        assert result is not None
        assert result.id == category_id
        mock_repo.get_by_id.assert_called_once_with(category_id)
