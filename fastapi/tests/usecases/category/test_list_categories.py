"""
list_categories.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.category.list_categories import ListCategoriesUseCase
from app.domain.category import Category
from app.repository.category_repository import CategoryRepository


class TestListCategoriesUseCase:
    """ListCategoriesUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでListCategoriesUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)

        # Act
        use_case = ListCategoriesUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_returns_multiple_categories(self):
        """正常系: 複数のカテゴリを取得する"""
        # Arrange
        expected_categories = [
            Category(category_id=1, name="カテゴリ1"),
            Category(category_id=2, name="カテゴリ2"),
            Category(category_id=3, name="カテゴリ3")
        ]
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.list_all.return_value = expected_categories
        
        use_case = ListCategoriesUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_categories
        assert len(result) == 3
        assert all(isinstance(category, Category) for category in result)
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_empty_list(self):
        """正常系: カテゴリが存在しない場合は空のリストを返す"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.list_all.return_value = []
        
        use_case = ListCategoriesUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == []
        assert len(result) == 0
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_single_category(self):
        """エッジケース: 単一のカテゴリを取得する"""
        # Arrange
        expected_categories = [Category(category_id=1, name="唯一のカテゴリ")]
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.list_all.return_value = expected_categories
        
        use_case = ListCategoriesUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_categories
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "唯一のカテゴリ"
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_returns_many_categories(self):
        """エッジケース: 大量のカテゴリを取得する"""
        # Arrange
        expected_categories = [
            Category(category_id=i, name=f"カテゴリ{i}")
            for i in range(1, 1001)  # 1000個のカテゴリ
        ]
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.list_all.return_value = expected_categories
        
        use_case = ListCategoriesUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_categories
        assert len(result) == 1000
        assert all(isinstance(category, Category) for category in result)
        mock_repo.list_all.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_preserves_category_order(self):
        """正常系: カテゴリの順序が保持される"""
        # Arrange
        expected_categories = [
            Category(category_id=5, name="5番目"),
            Category(category_id=1, name="1番目"),
            Category(category_id=3, name="3番目"),
            Category(category_id=2, name="2番目")
        ]
        
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.list_all.return_value = expected_categories
        
        use_case = ListCategoriesUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == expected_categories
        assert result[0].id == 5
        assert result[1].id == 1
        assert result[2].id == 3
        assert result[3].id == 2
        mock_repo.list_all.assert_called_once()
