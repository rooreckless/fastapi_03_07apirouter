"""Category DTO テストモジュール."""

import pytest
from pydantic import ValidationError
from app.dto.category_dto import CategoryCreateDTO, CategoryReadDTO, CategoryUpdateDTO


class TestCategoryCreateDTO:
    """CategoryCreateDTOのテストクラス."""

    def test_create_dto_success(self):
        """正常系: 正常なカテゴリ名でDTOが作成される."""
        dto = CategoryCreateDTO(category_name="テストカテゴリ")
        assert dto.category_name == "テストカテゴリ"

    def test_create_dto_with_empty_string(self):
        """エッジケース: 空文字列のカテゴリ名でDTOが作成される."""
        dto = CategoryCreateDTO(category_name="")
        assert dto.category_name == ""

    def test_create_dto_with_long_name(self):
        """エッジケース: 長いカテゴリ名でDTOが作成される."""
        long_name = "a" * 1000
        dto = CategoryCreateDTO(category_name=long_name)
        assert dto.category_name == long_name

    def test_create_dto_with_special_characters(self):
        """正常系: 特殊文字を含むカテゴリ名でDTOが作成される."""
        special_name = "カテゴリ-123_@#$%"
        dto = CategoryCreateDTO(category_name=special_name)
        assert dto.category_name == special_name

    def test_create_dto_with_unicode_characters(self):
        """正常系: Unicode文字を含むカテゴリ名でDTOが作成される."""
        unicode_name = "カテゴリ🚀✨"
        dto = CategoryCreateDTO(category_name=unicode_name)
        assert dto.category_name == unicode_name

    def test_create_dto_missing_category_name(self):
        """異常系: category_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateDTO()  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_name",)

    def test_create_dto_none_category_name(self):
        """異常系: category_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateDTO(category_name=None)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_create_dto_invalid_type(self):
        """異常系: category_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateDTO(category_name=123)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_create_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = CategoryCreateDTO(category_name="テストカテゴリ")
        result = dto.model_dump()
        assert result == {"category_name": "テストカテゴリ"}

    def test_create_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"category_name": "テストカテゴリ"}
        dto = CategoryCreateDTO(**data)
        assert dto.category_name == "テストカテゴリ"


class TestCategoryUpdateDTO:
    """CategoryUpdateDTOのテストクラス."""

    def test_update_dto_success(self):
        """正常系: 正常なカテゴリ名でDTOが作成される."""
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        assert dto.category_name == "更新されたカテゴリ"

    def test_update_dto_with_empty_string(self):
        """エッジケース: 空文字列のカテゴリ名でDTOが作成される."""
        dto = CategoryUpdateDTO(category_name="")
        assert dto.category_name == ""

    def test_update_dto_with_long_name(self):
        """エッジケース: 長いカテゴリ名でDTOが作成される."""
        long_name = "b" * 1000
        dto = CategoryUpdateDTO(category_name=long_name)
        assert dto.category_name == long_name

    def test_update_dto_with_special_characters(self):
        """正常系: 特殊文字を含むカテゴリ名でDTOが作成される."""
        special_name = "更新カテゴリ-456_&*()+"
        dto = CategoryUpdateDTO(category_name=special_name)
        assert dto.category_name == special_name

    def test_update_dto_missing_category_name(self):
        """異常系: category_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryUpdateDTO()  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_name",)

    def test_update_dto_none_category_name(self):
        """異常系: category_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryUpdateDTO(category_name=None)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_update_dto_invalid_type(self):
        """異常系: category_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryUpdateDTO(category_name=456)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_update_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = CategoryUpdateDTO(category_name="更新されたカテゴリ")
        result = dto.model_dump()
        assert result == {"category_name": "更新されたカテゴリ"}

    def test_update_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"category_name": "更新されたカテゴリ"}
        dto = CategoryUpdateDTO(**data)
        assert dto.category_name == "更新されたカテゴリ"


class TestCategoryReadDTO:
    """CategoryReadDTOのテストクラス."""

    def test_read_dto_success(self):
        """正常系: 正常なパラメータでDTOが作成される."""
        dto = CategoryReadDTO(category_id=1, category_name="テストカテゴリ")
        assert dto.category_id == 1
        assert dto.category_name == "テストカテゴリ"

    def test_read_dto_with_zero_id(self):
        """エッジケース: IDが0の場合でDTOが作成される."""
        dto = CategoryReadDTO(category_id=0, category_name="テストカテゴリ")
        assert dto.category_id == 0
        assert dto.category_name == "テストカテゴリ"

    def test_read_dto_with_negative_id(self):
        """エッジケース: 負のIDでDTOが作成される."""
        dto = CategoryReadDTO(category_id=-1, category_name="テストカテゴリ")
        assert dto.category_id == -1
        assert dto.category_name == "テストカテゴリ"

    def test_read_dto_with_large_id(self):
        """エッジケース: 大きなIDでDTOが作成される."""
        large_id = 2**31 - 1
        dto = CategoryReadDTO(category_id=large_id, category_name="テストカテゴリ")
        assert dto.category_id == large_id
        assert dto.category_name == "テストカテゴリ"

    def test_read_dto_with_empty_string_name(self):
        """エッジケース: 空文字列のカテゴリ名でDTOが作成される."""
        dto = CategoryReadDTO(category_id=1, category_name="")
        assert dto.category_id == 1
        assert dto.category_name == ""

    def test_read_dto_missing_category_id(self):
        """異常系: category_idが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_name="テストカテゴリ")  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_id",)

    def test_read_dto_missing_category_name(self):
        """異常系: category_nameが指定されていない場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_id=1)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "missing"
        assert errors[0]["loc"] == ("category_name",)

    def test_read_dto_none_category_id(self):
        """異常系: category_idがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_id=None, category_name="テストカテゴリ")  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "int_type"
        assert errors[0]["loc"] == ("category_id",)

    def test_read_dto_none_category_name(self):
        """異常系: category_nameがNoneの場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_id=1, category_name=None)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_read_dto_invalid_id_type(self):
        """異常系: category_idが文字列で型変換できない場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_id="invalid_number", category_name="テストカテゴリ")  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "int_parsing"
        assert errors[0]["loc"] == ("category_id",)

    def test_read_dto_invalid_name_type(self):
        """異常系: category_nameが文字列以外の場合."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryReadDTO(category_id=1, category_name=123)  # type: ignore
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_type"
        assert errors[0]["loc"] == ("category_name",)

    def test_read_dto_to_dict(self):
        """正常系: DTOが辞書形式に変換される."""
        dto = CategoryReadDTO(category_id=1, category_name="テストカテゴリ")
        result = dto.model_dump()
        expected = {
            "category_name": "テストカテゴリ",
            "category_id": 1,
            "created_by": None,
            "updated_by": None,
            "created_at": None,
            "updated_at": None
        }
        assert result == expected

    def test_read_dto_from_dict(self):
        """正常系: 辞書からDTOが作成される."""
        data = {"category_id": 1, "category_name": "テストカテゴリ"}
        dto = CategoryReadDTO(**data)
        assert dto.category_id == 1
        assert dto.category_name == "テストカテゴリ"

    def test_read_dto_config_from_attributes(self):
        """正常系: from_attributes設定が有効である."""
        # モックオブジェクトでfrom_attributes機能をテスト
        class MockORM:
            def __init__(self):
                self.category_id = 1
                self.category_name = "テストカテゴリ"
                self.created_by = None
                self.updated_by = None
                self.created_at = None
                self.updated_at = None
        
        mock_obj = MockORM()
        dto = CategoryReadDTO.model_validate(mock_obj)
        assert dto.category_id == 1
        assert dto.category_name == "テストカテゴリ"
        assert dto.created_by is None
        assert dto.updated_by is None
        assert dto.created_at is None
        assert dto.updated_at is None
