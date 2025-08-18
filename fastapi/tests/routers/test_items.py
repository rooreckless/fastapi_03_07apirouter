"""Item router テストモジュール."""

import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.routers.items import (
    get_item_repo,
    get_create_uc,
    get_list_uc,
    get_get_uc,
    get_update_uc,
    get_update_name_uc,
    get_delete_uc,
    create,
    list_all,
    get_item,
    update_item,
    update_name_body,
    update_name_dto,
    delete_item,
)
from app.dto.item_dto import ItemCreateDTO, ItemReadDTO, ItemUpdateDTO, ItemUpdateNameDTO
from app.domain.items.item import Item


class TestGetItemRepo:
    """get_item_repo関数のテストクラス."""

    def test_get_item_repo_success(self, mocker):
        """正常系: SQLAlchemyItemRepositoryインスタンスが正常に作成される."""
        mock_db = mocker.Mock()
        mock_repo_class = mocker.patch(
            "app.routers.items.SQLAlchemyItemRepository"
        )
        
        result = get_item_repo(mock_db)
        
        mock_repo_class.assert_called_once_with(mock_db)
        assert result == mock_repo_class.return_value


class TestGetCreateUc:
    """get_create_uc関数のテストクラス."""

    def test_get_create_uc_success(self, mocker):
        """正常系: CreateItemUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.CreateItemUseCase"
        )
        
        result = get_create_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetListUc:
    """get_list_uc関数のテストクラス."""

    def test_get_list_uc_success(self, mocker):
        """正常系: ListItemsUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.ListItemsUseCase"
        )
        
        result = get_list_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetGetUc:
    """get_get_uc関数のテストクラス."""

    def test_get_get_uc_success(self, mocker):
        """正常系: GetItemUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.GetItemUseCase"
        )
        
        result = get_get_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetUpdateUc:
    """get_update_uc関数のテストクラス."""

    def test_get_update_uc_success(self, mocker):
        """正常系: UpdateItemUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.UpdateItemUseCase"
        )
        
        result = get_update_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetUpdateNameUc:
    """get_update_name_uc関数のテストクラス."""

    def test_get_update_name_uc_success(self, mocker):
        """正常系: UpdateItemNameUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.UpdateItemNameUseCase"
        )
        
        result = get_update_name_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestGetDeleteUc:
    """get_delete_uc関数のテストクラス."""

    def test_get_delete_uc_success(self, mocker):
        """正常系: DeleteItemUseCaseインスタンスが正常に作成される."""
        mock_repo = mocker.Mock()
        mock_uc_class = mocker.patch(
            "app.routers.items.DeleteItemUseCase"
        )
        
        result = get_delete_uc(mock_repo)
        
        mock_uc_class.assert_called_once_with(mock_repo)
        assert result == mock_uc_class.return_value


class TestCreate:
    """create関数のテストクラス."""

    @pytest.mark.anyio
    async def test_create_success_with_categories(self, mocker):
        """正常系: カテゴリありでアイテムが正常に作成される."""
        dto = ItemCreateDTO(item_name="テストアイテム", category_ids=[1, 2])
        mock_item = Item(
            item_id=1,
            name="テストアイテム",
            category_ids=[1, 2]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await create(dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with("テストアイテム", [1, 2])
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "テストアイテム"
        assert result.category_ids == [1, 2]

    @pytest.mark.anyio
    async def test_create_success_without_categories(self, mocker):
        """正常系: カテゴリなしでアイテムが正常に作成される."""
        dto = ItemCreateDTO(item_name="テストアイテム", category_ids=None)
        mock_item = Item(
            item_id=1,
            name="テストアイテム",
            category_ids=[]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await create(dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with("テストアイテム", [])
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "テストアイテム"
        assert result.category_ids == []

    @pytest.mark.anyio
    async def test_create_with_empty_category_list(self, mocker):
        """エッジケース: 空のカテゴリリストでアイテムを作成."""
        dto = ItemCreateDTO(item_name="テストアイテム", category_ids=[])
        mock_item = Item(
            item_id=1,
            name="テストアイテム",
            category_ids=[]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await create(dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with("テストアイテム", [])
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "テストアイテム"
        assert result.category_ids == []

    @pytest.mark.anyio
    async def test_create_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        dto = ItemCreateDTO(item_name="テストアイテム", category_ids=[1])
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await create(dto, mock_uc)


class TestListAll:
    """list_all関数のテストクラス."""

    @pytest.mark.anyio
    async def test_list_all_success(self, mocker):
        """正常系: アイテム一覧が正常に取得される."""
        mock_items = [
            Item(item_id=1, name="アイテム1", category_ids=[1]),
            Item(item_id=2, name="アイテム2", category_ids=[2, 3])
        ]
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_items
        
        result = await list_all(mock_uc)
        
        mock_uc.execute.assert_called_once()
        assert len(result) == 2
        assert all(isinstance(item, ItemReadDTO) for item in result)
        assert result[0].item_id == 1
        assert result[0].item_name == "アイテム1"
        assert result[0].category_ids == [1]
        assert result[1].item_id == 2
        assert result[1].item_name == "アイテム2"
        assert result[1].category_ids == [2, 3]

    @pytest.mark.anyio
    async def test_list_all_empty_result(self, mocker):
        """エッジケース: 空のアイテム一覧が返される."""
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


class TestGetItem:
    """get_item関数のテストクラス."""

    @pytest.mark.anyio
    async def test_get_item_success(self, mocker):
        """正常系: アイテムが正常に取得される."""
        item_id = 1
        mock_item = Item(
            item_id=1,
            name="テストアイテム",
            category_ids=[1, 2]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await get_item(item_id, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1)
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "テストアイテム"
        assert result.category_ids == [1, 2]

    @pytest.mark.anyio
    async def test_get_item_not_found(self, mocker):
        """異常系: アイテムが見つからない場合."""
        item_id = 999
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(999)

    @pytest.mark.anyio
    async def test_get_item_zero_id(self, mocker):
        """エッジケース: IDが0の場合."""
        item_id = 0
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(0)

    @pytest.mark.anyio
    async def test_get_item_negative_id(self, mocker):
        """エッジケース: 負のIDの場合."""
        item_id = -1
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(-1)

    @pytest.mark.anyio
    async def test_get_item_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        item_id = 1
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await get_item(item_id, mock_uc)


class TestUpdateItem:
    """update_item関数のテストクラス."""

    @pytest.mark.anyio
    async def test_update_item_success(self, mocker):
        """正常系: アイテムが正常に更新される."""
        item_id = 1
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[1, 3])
        mock_item = Item(
            item_id=1,
            name="更新されたアイテム",
            category_ids=[1, 3]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_item(item_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "更新されたアイテム", [1, 3])
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "更新されたアイテム"
        assert result.category_ids == [1, 3]

    @pytest.mark.anyio
    async def test_update_item_not_found(self, mocker):
        """異常系: 更新対象のアイテムが見つからない場合."""
        item_id = 999
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[1])
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_item(item_id, dto, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(999, "更新されたアイテム", [1])

    @pytest.mark.anyio
    async def test_update_item_with_none_categories(self, mocker):
        """エッジケース: カテゴリIDsがNoneでアイテムを更新."""
        item_id = 1
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=None)
        mock_item = Item(
            item_id=1,
            name="更新されたアイテム",
            category_ids=[]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_item(item_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "更新されたアイテム", None)
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "更新されたアイテム"

    @pytest.mark.anyio
    async def test_update_item_usecase_raises_exception(self, mocker):
        """異常系: ユースケースで例外が発生する場合."""
        item_id = 1
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[1])
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await update_item(item_id, dto, mock_uc)


class TestUpdateNameBody:
    """update_name_body関数のテストクラス."""

    @pytest.mark.anyio
    async def test_update_name_body_success(self, mocker):
        """正常系: アイテム名が正常に更新される（Body使用）."""
        item_id = 1
        new_name = "新しい名前"
        mock_item = Item(
            item_id=1,
            name="新しい名前",
            category_ids=[1]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_name_body(item_id, new_name, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "新しい名前")
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "新しい名前"
        assert result.category_ids == [1]

    @pytest.mark.anyio
    async def test_update_name_body_item_not_found(self, mocker):
        """異常系: アイテムが見つからない場合（ValueError）."""
        item_id = 999
        new_name = "新しい名前"
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = ValueError("Item not found")
        
        with pytest.raises(HTTPException) as exc_info:
            await update_name_body(item_id, new_name, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(999, "新しい名前")

    @pytest.mark.anyio
    async def test_update_name_body_with_empty_name(self, mocker):
        """エッジケース: 空文字列でアイテム名を更新."""
        item_id = 1
        new_name = ""
        mock_item = Item(
            item_id=1,
            name="",
            category_ids=[1]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_name_body(item_id, new_name, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "")
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == ""

    @pytest.mark.anyio
    async def test_update_name_body_other_exception(self, mocker):
        """異常系: ValueError以外の例外が発生する場合."""
        item_id = 1
        new_name = "新しい名前"
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await update_name_body(item_id, new_name, mock_uc)


class TestUpdateNameDto:
    """update_name_dto関数のテストクラス."""

    @pytest.mark.anyio
    async def test_update_name_dto_success(self, mocker):
        """正常系: アイテム名が正常に更新される（DTO使用）."""
        item_id = 1
        dto = ItemUpdateNameDTO(item_name="新しい名前")
        mock_item = Item(
            item_id=1,
            name="新しい名前",
            category_ids=[1]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_name_dto(item_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "新しい名前")
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == "新しい名前"
        assert result.category_ids == [1]

    @pytest.mark.anyio
    async def test_update_name_dto_item_not_found(self, mocker):
        """異常系: アイテムが見つからない場合（ValueError）."""
        item_id = 999
        dto = ItemUpdateNameDTO(item_name="新しい名前")
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = ValueError("Item not found")
        
        with pytest.raises(HTTPException) as exc_info:
            await update_name_dto(item_id, dto, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
        mock_uc.execute.assert_called_once_with(999, "新しい名前")

    @pytest.mark.anyio
    async def test_update_name_dto_with_empty_name(self, mocker):
        """エッジケース: 空文字列でアイテム名を更新."""
        item_id = 1
        dto = ItemUpdateNameDTO(item_name="")
        mock_item = Item(
            item_id=1,
            name="",
            category_ids=[1]
        )
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = mock_item
        
        result = await update_name_dto(item_id, dto, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1, "")
        assert isinstance(result, ItemReadDTO)
        assert result.item_id == 1
        assert result.item_name == ""

    @pytest.mark.anyio
    async def test_update_name_dto_other_exception(self, mocker):
        """異常系: ValueError以外の例外が発生する場合."""
        item_id = 1
        dto = ItemUpdateNameDTO(item_name="新しい名前")
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await update_name_dto(item_id, dto, mock_uc)


class TestDeleteItem:
    """delete_item関数のテストクラス."""

    @pytest.mark.anyio
    async def test_delete_item_success(self, mocker):
        """正常系: アイテムが正常に削除される."""
        item_id = 1
        mock_uc = AsyncMock()
        mock_uc.execute.return_value = None
        
        result = await delete_item(item_id, mock_uc)
        
        mock_uc.execute.assert_called_once_with(1)
        assert result is None

    @pytest.mark.anyio
    async def test_delete_item_not_found(self, mocker):
        """異常系: 削除対象のアイテムが見つからない場合."""
        item_id = 999
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = ValueError("Item not found")
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "str(e)"
        mock_uc.execute.assert_called_once_with(999)

    @pytest.mark.anyio
    async def test_delete_item_zero_id(self, mocker):
        """エッジケース: IDが0の場合の削除."""
        item_id = 0
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = ValueError("Item not found")
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        mock_uc.execute.assert_called_once_with(0)

    @pytest.mark.anyio
    async def test_delete_item_negative_id(self, mocker):
        """エッジケース: 負のIDの場合の削除."""
        item_id = -1
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = ValueError("Item not found")
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_item(item_id, mock_uc)
        
        assert exc_info.value.status_code == 404
        mock_uc.execute.assert_called_once_with(-1)

    @pytest.mark.anyio
    async def test_delete_item_other_exception(self, mocker):
        """異常系: ValueError以外の例外が発生する場合."""
        item_id = 1
        mock_uc = AsyncMock()
        mock_uc.execute.side_effect = Exception("データベースエラー")
        
        with pytest.raises(Exception, match="データベースエラー"):
            await delete_item(item_id, mock_uc)
