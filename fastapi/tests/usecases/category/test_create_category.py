"""
create_category.pyのテストモジュール
"""

import pytest
from unittest.mock import AsyncMock
from app.usecases.category.create_category import CreateCategoryUseCase
from app.domain.category import Category
from app.abstract_repository.category_repository import CategoryRepository


class TestCreateCategoryUseCase:
    """CreateCategoryUseCaseクラスのテストクラス"""

    def test_init_with_repository(self):
        """正常系: リポジトリでCreateCategoryUseCaseを初期化する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)

        # Act
        use_case = CreateCategoryUseCase(mock_repo)

        # Assert
        assert use_case.repo == mock_repo

    @pytest.mark.anyio
    async def test_execute_creates_category_successfully(self):
        """正常系: カテゴリを正常に作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 1
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=1,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=1,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = "テストカテゴリ"

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 1
        assert result.name == category_name
        assert result.created_by == 1
        assert result.updated_by == 1
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()
        mock_repo.get_by_id.assert_called_with(1)
        
        # saveに渡されたカテゴリを検証
        saved_category = mock_repo.save.call_args[0][0]
        assert saved_category.id == 1
        assert saved_category.name == category_name

    @pytest.mark.anyio
    async def test_execute_with_empty_name(self):
        """エッジケース: 空の名前でカテゴリを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 2
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=2,
            name="",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = ""

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 2
        assert result.name == ""
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_long_name(self):
        """エッジケース: 長い名前でカテゴリを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 3
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        category_name = "a" * 1000  # 1000文字の長い名前
        mock_category = Category(
            category_id=3,
            name=category_name,
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 3
        assert result.name == category_name
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_special_characters_name(self):
        """エッジケース: 特殊文字を含む名前でカテゴリを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 4
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=4,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

        # get_by_idが返すモックカテゴリを設定  
        mock_category = Category(
            category_id=4,
            name=category_name,
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 4
        assert result.name == category_name
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_unicode_name(self):
        """エッジケース: Unicode文字を含む名前でカテゴリを作成する"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 5
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=5,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = "テスト🐶🐱🎉カテゴリ"

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=5,
            name=category_name,
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 5
        assert result.name == category_name
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_zero_id_from_repository(self):
        """エッジケース: リポジトリから0のIDが返される場合"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 0
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=0,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = "テストカテゴリ"

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 0
        assert result.name == category_name
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()

    @pytest.mark.anyio
    async def test_execute_with_large_id_from_repository(self):
        """エッジケース: リポジトリから大きなIDが返される場合"""
        # Arrange
        mock_repo = AsyncMock(spec=CategoryRepository)
        mock_repo.next_identifier.return_value = 999999999
        mock_repo.save.return_value = None

        # get_by_idが返すモックカテゴリを設定
        mock_category = Category(
            category_id=999999999,
            name="テストカテゴリ",
            created_by=1,
            updated_by=1
        )
        mock_repo.get_by_id.return_value = mock_category
        
        use_case = CreateCategoryUseCase(mock_repo)
        category_name = "テストカテゴリ"

        # Act
        result = await use_case.execute(category_name, 1)

        # Assert
        assert isinstance(result, Category)
        assert result.id == 999999999
        assert result.name == category_name
        mock_repo.next_identifier.assert_called_once()
        mock_repo.save.assert_called_once()
