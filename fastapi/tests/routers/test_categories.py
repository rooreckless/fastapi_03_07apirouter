"""Category router テストモジュール."""

import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.routers.categories import (
    get_category_repo,
    get_create_uc,
    get_list_uc,
    get_get_uc,
    get_update_uc,
    create,
    list_all,
    get_category,
    update_category,
)
from app.dto.category_dto import CategoryCreateDTO, CategoryReadDTO, CategoryUpdateDTO
from app.domain.category.category import Category


class TestGetCategoryRepo:
    """get_category_repo関数のテストクラス."""

    def test_get_category_repo_success(self, mocker):
        """正常系: SQLAlchemyCategoryRepositoryインスタンスが正常に作成される."""
        mock_db = mocker.Mock()
        mock_repo_class = mocker.patch(
            "app.routers.categories.SQLAlchemyCategoryRepository"
        )
        
        result = get_category_repo(mock_db)
        
        mock_repo_class.assert_called_once_with(mock_db)
        assert result == mock_repo_class.return_value


class TestGetCreateUc:
    """get_create_uc関数のテストクラス."""

    def test_get_create_uc_success(self, mocker):
        """正常系: CreateCategoryUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.categories.CreateCategoryUseCase"
        )
        
        result = get_create_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetListUc:
    """get_list_uc関数のテストクラス."""

    def test_get_list_uc_success(self, mocker):
        """正常系: ListCategoriesUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.categories.ListCategoriesUseCase"
        )
        
        result = get_list_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetGetUc:
    """get_get_uc関数のテストクラス."""

    def test_get_get_uc_success(self, mocker):
        """正常系: GetCategoryUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.categories.GetCategoryUseCase"
        )
        
        result = get_get_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetUpdateUc:
    """get_update_uc関数のテストクラス."""

    def test_get_update_uc_success(self, mocker):
        """正常系: UpdateCategoryUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.categories.UpdateCategoryUseCase"
        )
        
        result = get_update_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestCreate:
    """create関数のテストクラス."""

    @pytest.mark.anyio
    async def test_create_success(self, mocker):
        """正常系: カテゴリが正常に作成される."""
        dto = CategoryCreateDTO(category_name="テストカテゴリ")
        mock_category = Category(
            category_id=1,
            name="テストカテゴリ"
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_category
        
        result = await create(dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with("テストカテゴリ")
        assert isinstance(result, CategoryReadDTO)
        assert result.category_id == 1
        assert result.category_name == "テストカテゴリ"

    @pytest.mark.anyio
    async def test_create_with_empty_name(self, mocker):
        """エッジケース: 空文字列のカテゴリ名でカテゴリを作成."""
        dto = CategoryCreateDTO(category_name="")
        mock_category = Category(
            category_id=1,
            name=""
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_category
        
        result = await create(dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with("")
        assert isinstance(result, CategoryReadDTO)
        assert result.category_id == 1
        assert result.category_name == ""

    @pytest.mark.anyio
    async def test_create_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        dto = CategoryCreateDTO(category_name="テストカテゴリ")
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await create(dto, mock_uc)


class TestListAll:
    """list_all関数のテストクラス."""

    @pytest.mark.anyio
    async def test_list_all_success(self, mocker):
        """正常系: カテゴリ一覧が正常に取得される."""
        mock_categories = [
            Category(category_id=1, name="カテゴリ1"),
            Category(category_id=2, name="カテゴリ2")
        ]
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_categories
        
        result = await list_all(mock_uc)
        
        mock_uc.execute.assert_called_once()
        assert len(result) == 2
        assert all(isinstance(item, CategoryReadDTO) for item in result)
        assert result[0].category_id == 1
        assert result[0].category_name == "カテゴリ1"
        assert result[1].category_id == 2
        assert result[1].category_name == "カテゴリ2"

    @pytest.mark.anyio
    async def test_list_all_empty_result(self, mocker):
        """エッジケース: 空のカテゴリ一覧が返される."""
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = []
        
        result = await list_all(mock_uc)
        
        mock_uc.execute.assert_called_once()
        assert result == []

    @pytest.mark.anyio
    async def test_list_all_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await list_all(mock_uc)


class TestGetCategory:
    """get_category関数のテストクラス."""

    @pytest.mark.anyio
    async def test_get_category_success(self, mocker):
        """正常系: カテゴリが正常に取得される."""
        category_id = 1
        mock_category = Category(
            category_id=1,
            name="テストカテゴリ"
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_category
        
        result = await get_category(category_id, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1)
        assert isinstance(result, CategoryReadDTO)
        assert result.category_id == 1
        assert result.category_name == "テストカテゴリ"

    @pytest.mark.anyio
    async def test_get_category_not_found(self, mocker):
        """異常系: カテゴリが見つからない場合."""
        category_id = 999
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_category(category_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_uc.execute.assert_called_once_with(999)

    @pytest.mark.anyio
    async def test_get_category_zero_id(self, mocker):
        """エッジケース: IDが0の場合."""
        category_id = 0
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_category(category_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_uc.execute.assert_called_once_with(0)

    @pytest.mark.anyio
    async def test_get_category_negative_id(self, mocker):
        """エッジケース: 負のIDの場合."""
        category_id = -1
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_category(category_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_uc.execute.assert_called_once_with(-1)

    @pytest.mark.anyio
    async def test_get_category_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        category_id = 1
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await get_category(category_id, mock_uc)


class TestUpdateCategory:
    """update_category関数のテストクラス."""

    @pytest.mark.anyio
    async def test_update_category_success(self, mocker):
        """正常系: カテゴリが正常に更新される."""
        category_id = 1
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        mock_category = Category(
            category_id=1,
            name="更新されたカテゴリ"
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_category
        
        result = await update_category(category_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "更新されたカテゴリ")
        assert isinstance(result, CategoryReadDTO)
        assert result.category_id == 1
        assert result.category_name == "更新されたカテゴリ"

    @pytest.mark.anyio
    async def test_update_category_not_found(self, mocker):
        """異常系: 更新対象のカテゴリが見つからない場合."""
        category_id = 999
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_category(category_id, dto, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_uc.execute.assert_called_once_with(999, "更新されたカテゴリ")

    @pytest.mark.anyio
    async def test_update_category_with_empty_name(self, mocker):
        """エッジケース: 空文字列でカテゴリ名を更新."""
        category_id = 1
        dto = CategoryUpdateDTO(category_name="")
        mock_category = Category(
            category_id=1,
            name=""
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_category
        
        result = await update_category(category_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "")
        assert isinstance(result, CategoryReadDTO)
        assert result.category_id == 1
        assert result.category_name == ""

    @pytest.mark.anyio
    async def test_update_category_zero_id(self, mocker):
        """エッジケース: IDが0の場合の更新."""
        category_id = 0
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_category(category_id, dto, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_uc.execute.assert_called_once_with(0, "更新されたカテゴリ")

    @pytest.mark.anyio
    async def test_update_category_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        category_id = 1
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await update_category(category_id, dto, mock_uc)
