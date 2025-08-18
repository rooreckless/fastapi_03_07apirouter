"""Item DTO テストモジュール."""

import pytest
from pydantic import ValidationError
from app.dto.item_dto import ItemBase, ItemCreateDTO, ItemUpdateDTO, ItemUpdateNameDTO, ItemReadDTO


class TestItemBase:
    """ItemBaseのテストクラス."""

    def test_item_base_success_with_categories(self):
        """正常系: カテゴリIDsありでItemBaseが作成される."""
        item = ItemBase(item_name="テストアイテム", category_ids=[1, 2, 3])
        assert item.item_name == "テストアイテム"
        assert item.category_ids == [1, 2, 3]

    def test_item_base_success_without_categories(self):
        """正常系: カテゴリIDsなしでItemBaseが作成される."""
        item = ItemBase(item_name="テストアイテム", category_ids=None)
        assert item.item_name == "テストアイテム"
        assert item.category_ids is None

    def test_item_base_with_empty_category_list(self):
        """エッジケース: 空のカテゴリリストでItemBaseが作成される."""
        item = ItemBase(item_name="テストアイテム", category_ids=[])
        assert item.item_name == "テストアイテム"
        assert item.category_ids == []

    def test_item_base_with_single_category(self):
        """正常系: 単一カテゴリでItemBaseが作成される."""
        item = ItemBase(item_name="テストアイテム", category_ids=[1])
        assert item.item_name == "テストアイテム"
        assert item.category_ids == [1]

    def test_item_base_with_duplicate_categories(self):
        """エッジケース: 重複するカテゴリIDsでItemBaseが作成される."""
        item = ItemBase(item_name="テストアイテム", category_ids=[1, 1, 2, 2])
        assert item.item_name == "テストアイテム"
        assert item.category_ids == [1, 1, 2, 2]

    def test_item_base_missing_item_name(self):
        """異常系: item_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(category_ids=[1, 2])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("item_name",)

    def test_item_base_missing_category_ids(self):
        """異常系: category_idsが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(item_name="テストアイテム")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_ids",)

    def test_item_base_none_item_name(self):
        """異常系: item_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(item_name=None, category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_item_base_invalid_item_name_type(self):
        """異常系: item_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(item_name=123, category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_item_base_invalid_category_ids_type(self):
        """異常系: category_idsがリストまたはNone以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(item_name="テストアイテム", category_ids="invalid")
        
        errors = exc_info.value.errors()
        assert len(errors) >= 1

    def test_item_base_invalid_category_id_type(self):
        """異常系: category_idsの要素が文字列で変換できない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemBase(item_name="テストアイテム", category_ids=["invalid", "number"])
        
        errors = exc_info.value.errors()
        assert len(errors) >= 1


class TestItemCreateDTO:
    """ItemCreateDTOのテストクラス."""

    def test_create_dto_success_with_categories(self):
        """正常系: カテゴリIDsありでDTOが作成される."""
        dto = ItemCreateDTO(item_name="新しいアイテム", category_ids=[1, 2])
        assert dto.item_name == "新しいアイテム"
        assert dto.category_ids == [1, 2]

    def test_create_dto_success_without_categories(self):
        """正常系: カテゴリIDsなしでDTOが作成される."""
        dto = ItemCreateDTO(item_name="新しいアイテム", category_ids=None)
        assert dto.item_name == "新しいアイテム"
        assert dto.category_ids is None

    def test_create_dto_with_empty_category_list(self):
        """エッジケース: 空のカテゴリリストでDTOが作成される."""
        dto = ItemCreateDTO(item_name="新しいアイテム", category_ids=[])
        assert dto.item_name == "新しいアイテム"
        assert dto.category_ids == []

    def test_create_dto_with_empty_name(self):
        """エッジケース: 空文字列のアイテム名でDTOが作成される."""
        dto = ItemCreateDTO(item_name="", category_ids=[1])
        assert dto.item_name == ""
        assert dto.category_ids == [1]

    def test_create_dto_with_long_name(self):
        """エッジケース: 長いアイテム名でDTOが作成される."""
        long_name = "a" * 1000
        dto = ItemCreateDTO(item_name=long_name, category_ids=[1])
        assert dto.item_name == long_name
        assert dto.category_ids == [1]

    def test_create_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = ItemCreateDTO(item_name="新しいアイテム", category_ids=[1, 2])
        result = dto.model_dump()
        assert result == {"item_name": "新しいアイテム", "category_ids": [1, 2]}

    def test_create_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"item_name": "新しいアイテム", "category_ids": [1, 2]}
        dto = ItemCreateDTO(**data)
        assert dto.item_name == "新しいアイテム"
        assert dto.category_ids == [1, 2]


class TestItemUpdateDTO:
    """ItemUpdateDTOのテストクラス."""

    def test_update_dto_success_with_categories(self):
        """正常系: カテゴリIDsありでDTOが作成される."""
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[2, 3])
        assert dto.item_name == "更新されたアイテム"
        assert dto.category_ids == [2, 3]

    def test_update_dto_success_without_categories(self):
        """正常系: カテゴリIDsなしでDTOが作成される."""
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=None)
        assert dto.item_name == "更新されたアイテム"
        assert dto.category_ids is None

    def test_update_dto_with_empty_category_list(self):
        """エッジケース: 空のカテゴリリストでDTOが作成される."""
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[])
        assert dto.item_name == "更新されたアイテム"
        assert dto.category_ids == []

    def test_update_dto_with_empty_name(self):
        """エッジケース: 空文字列のアイテム名でDTOが作成される."""
        dto = ItemUpdateDTO(item_name="", category_ids=[1])
        assert dto.item_name == ""
        assert dto.category_ids == [1]

    def test_update_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = ItemUpdateDTO(item_name="更新されたアイテム", category_ids=[2, 3])
        result = dto.model_dump()
        assert result == {"item_name": "更新されたアイテム", "category_ids": [2, 3]}

    def test_update_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"item_name": "更新されたアイテム", "category_ids": [2, 3]}
        dto = ItemUpdateDTO(**data)
        assert dto.item_name == "更新されたアイテム"
        assert dto.category_ids == [2, 3]


class TestItemUpdateNameDTO:
    """ItemUpdateNameDTOのテストクラス."""

    def test_update_name_dto_success(self):
        """正常系: 正常なアイテム名でDTOが作成される."""
        dto = ItemUpdateNameDTO(item_name="新しい名前")
        assert dto.item_name == "新しい名前"

    def test_update_name_dto_with_empty_name(self):
        """エッジケース: 空文字列のアイテム名でDTOが作成される."""
        dto = ItemUpdateNameDTO(item_name="")
        assert dto.item_name == ""

    def test_update_name_dto_with_long_name(self):
        """エッジケース: 長いアイテム名でDTOが作成される."""
        long_name = "b" * 1000
        dto = ItemUpdateNameDTO(item_name=long_name)
        assert dto.item_name == long_name

    def test_update_name_dto_with_special_characters(self):
        """正常系: 特殊文字を含むアイテム名でDTOが作成される."""
        special_name = "アイテム-123_@#$%"
        dto = ItemUpdateNameDTO(item_name=special_name)
        assert dto.item_name == special_name

    def test_update_name_dto_missing_item_name(self):
        """異常系: item_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdateNameDTO()
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("item_name",)

    def test_update_name_dto_none_item_name(self):
        """異常系: item_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdateNameDTO(item_name=None)
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_update_name_dto_invalid_type(self):
        """異常系: item_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdateNameDTO(item_name=123)
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_update_name_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = ItemUpdateNameDTO(item_name="新しい名前")
        result = dto.model_dump()
        assert result == {"item_name": "新しい名前"}

    def test_update_name_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"item_name": "新しい名前"}
        dto = ItemUpdateNameDTO(**data)
        assert dto.item_name == "新しい名前"


class TestItemReadDTO:
    """ItemReadDTOのテストクラス."""

    def test_read_dto_success_with_categories(self):
        """正常系: カテゴリIDsありでDTOが作成される."""
        dto = ItemReadDTO(item_id=1, item_name="テストアイテム", category_ids=[1, 2])
        assert dto.item_id == 1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1, 2]

    def test_read_dto_success_without_categories(self):
        """正常系: カテゴリIDsなしでDTOが作成される."""
        dto = ItemReadDTO(item_id=1, item_name="テストアイテム", category_ids=None)
        assert dto.item_id == 1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids is None

    def test_read_dto_with_empty_category_list(self):
        """エッジケース: 空のカテゴリリストでDTOが作成される."""
        dto = ItemReadDTO(item_id=1, item_name="テストアイテム", category_ids=[])
        assert dto.item_id == 1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == []

    def test_read_dto_with_zero_id(self):
        """エッジケース: IDが0の場合でDTOが作成される."""
        dto = ItemReadDTO(item_id=0, item_name="テストアイテム", category_ids=[1])
        assert dto.item_id == 0
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1]

    def test_read_dto_with_negative_id(self):
        """エッジケース: 負のIDでDTOが作成される."""
        dto = ItemReadDTO(item_id=-1, item_name="テストアイテム", category_ids=[1])
        assert dto.item_id == -1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1]

    def test_read_dto_with_large_id(self):
        """エッジケース: 大きなIDでDTOが作成される."""
        large_id = 2**31 - 1
        dto = ItemReadDTO(item_id=large_id, item_name="テストアイテム", category_ids=[1])
        assert dto.item_id == large_id
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1]

    def test_read_dto_with_empty_name(self):
        """エッジケース: 空文字列のアイテム名でDTOが作成される."""
        dto = ItemReadDTO(item_id=1, item_name="", category_ids=[1])
        assert dto.item_id == 1
        assert dto.item_name == ""
        assert dto.category_ids == [1]

    def test_read_dto_missing_item_id(self):
        """異常系: item_idが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_name="テストアイテム", category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("item_id",)

    def test_read_dto_missing_item_name(self):
        """異常系: item_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id=1, category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("item_name",)

    def test_read_dto_missing_category_ids(self):
        """異常系: category_idsが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id=1, item_name="テストアイテム")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_ids",)

    def test_read_dto_none_item_id(self):
        """異常系: item_idがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id=None, item_name="テストアイテム", category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "int_type"
        assert errors[0]["loc"] == ("item_id",)

    def test_read_dto_none_item_name(self):
        """異常系: item_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id=1, item_name=None, category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_read_dto_invalid_id_type(self):
        """異常系: item_idが整数に変換できない場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id="invalid", item_name="テストアイテム", category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1

    def test_read_dto_invalid_name_type(self):
        """異常系: item_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            ItemReadDTO(item_id=1, item_name=123, category_ids=[1])
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("item_name",)

    def test_read_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = ItemReadDTO(item_id=1, item_name="テストアイテム", category_ids=[1, 2])
        result = dto.model_dump()
        assert result == {"item_id": 1, "item_name": "テストアイテム", "category_ids": [1, 2]}

    def test_read_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"item_id": 1, "item_name": "テストアイテム", "category_ids": [1, 2]}
        dto = ItemReadDTO(**data)
        assert dto.item_id == 1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1, 2]

    def test_read_dto_config_from_attributes(self):
        """正常系: from_attributes設定が有効である."""
        # モックオブジェクトでfrom_attributes機能をテスト
        class MockORM:
            def __init__(self):
                self.item_id = 1
                self.item_name = "テストアイテム"
                self.category_ids = [1, 2]
        
        mock_obj = MockORM()
        dto = ItemReadDTO.model_validate(mock_obj)
        assert dto.item_id == 1
        assert dto.item_name == "テストアイテム"
        assert dto.category_ids == [1, 2]
