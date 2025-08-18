"""
value_objects.pyのテストモジュール
"""

import pytest
from app.domain.items.value_objects import ItemName, CategoryId


class TestItemName:
    """ItemNameクラスのテストクラス"""

    def test_init_with_valid_name(self):
        """正常系: 有効な名前でItemNameを初期化する"""
        # Arrange
        name_value = "有効なアイテム名"

        # Act
        item_name = ItemName(name_value)

        # Assert
        assert item_name.value == name_value

    def test_init_with_name_containing_whitespace(self):
        """正常系: 前後に空白を含む名前でItemNameを初期化する（空白が削除される）"""
        # Arrange
        name_value = "  前後に空白があるアイテム名  "
        expected_value = "前後に空白があるアイテム名"

        # Act
        item_name = ItemName(name_value)

        # Assert
        assert item_name.value == expected_value

    def test_init_with_single_character_name(self):
        """エッジケース: 1文字の名前でItemNameを初期化する"""
        # Arrange
        name_value = "A"

        # Act
        item_name = ItemName(name_value)

        # Assert
        assert item_name.value == name_value

    def test_init_with_200_character_name(self):
        """エッジケース: 200文字ちょうどの名前でItemNameを初期化する"""
        # Arrange
        name_value = "a" * 200

        # Act
        item_name = ItemName(name_value)

        # Assert
        assert item_name.value == name_value
        assert len(item_name.value) == 200

    def test_init_with_empty_string_raises_error(self):
        """異常系: 空文字列でItemNameを初期化するとValueErrorが発生する"""
        # Arrange
        name_value = ""

        # Act & Assert
        with pytest.raises(ValueError, match="アイテム名は空にできません"):
            ItemName(name_value)

    def test_init_with_whitespace_only_raises_error(self):
        """異常系: 空白のみの文字列でItemNameを初期化するとValueErrorが発生する"""
        # Arrange
        name_value = "   "

        # Act & Assert
        with pytest.raises(ValueError, match="アイテム名は空にできません"):
            ItemName(name_value)

    def test_init_with_201_character_name_raises_error(self):
        """異常系: 201文字の名前でItemNameを初期化するとValueErrorが発生する"""
        # Arrange
        name_value = "a" * 201

        # Act & Assert
        with pytest.raises(ValueError, match="アイテム名は200文字以内である必要があります"):
            ItemName(name_value)

    def test_init_with_none_raises_error(self):
        """異常系: NoneでItemNameを初期化するとValueErrorが発生する"""
        # Act & Assert
        with pytest.raises(ValueError, match="アイテム名は空にできません"):
            ItemName(None)  # type: ignore

    def test_equality_with_same_value(self):
        """正常系: 同じ値を持つItemNameオブジェクトは等価である"""
        # Arrange
        name_value = "同じアイテム名"
        item_name1 = ItemName(name_value)
        item_name2 = ItemName(name_value)

        # Act & Assert
        assert item_name1 == item_name2

    def test_equality_with_different_value(self):
        """正常系: 異なる値を持つItemNameオブジェクトは等価でない"""
        # Arrange
        item_name1 = ItemName("アイテム名1")
        item_name2 = ItemName("アイテム名2")

        # Act & Assert
        assert item_name1 != item_name2

    def test_equality_with_non_item_name_object(self):
        """正常系: ItemNameオブジェクトと他の型のオブジェクトは等価でない"""
        # Arrange
        item_name = ItemName("アイテム名")
        other_object = "アイテム名"

        # Act & Assert
        assert item_name != other_object

    def test_hash_consistency(self):
        """正常系: 同じ値を持つItemNameオブジェクトは同じハッシュ値を持つ"""
        # Arrange
        name_value = "ハッシュテスト"
        item_name1 = ItemName(name_value)
        item_name2 = ItemName(name_value)

        # Act & Assert
        assert hash(item_name1) == hash(item_name2)

    def test_hash_different_for_different_values(self):
        """正常系: 異なる値を持つItemNameオブジェクトは異なるハッシュ値を持つ"""
        # Arrange
        item_name1 = ItemName("ハッシュテスト1")
        item_name2 = ItemName("ハッシュテスト2")

        # Act & Assert
        assert hash(item_name1) != hash(item_name2)

    def test_str_representation(self):
        """正常系: ItemNameの文字列表現は値と同じである"""
        # Arrange
        name_value = "文字列表現テスト"
        item_name = ItemName(name_value)

        # Act & Assert
        assert str(item_name) == name_value


class TestCategoryId:
    """CategoryIdクラスのテストクラス"""

    def test_init_with_positive_integer(self):
        """正常系: 正の整数でCategoryIdを初期化する"""
        # Arrange
        category_id_value = 5

        # Act
        category_id = CategoryId(category_id_value)

        # Assert
        assert category_id.value == category_id_value

    def test_init_with_one(self):
        """エッジケース: 1でCategoryIdを初期化する"""
        # Arrange
        category_id_value = 1

        # Act
        category_id = CategoryId(category_id_value)

        # Assert
        assert category_id.value == 1

    def test_init_with_large_integer(self):
        """エッジケース: 大きな正の整数でCategoryIdを初期化する"""
        # Arrange
        category_id_value = 999999999

        # Act
        category_id = CategoryId(category_id_value)

        # Assert
        assert category_id.value == category_id_value

    def test_init_with_zero_raises_error(self):
        """異常系: 0でCategoryIdを初期化するとValueErrorが発生する"""
        # Arrange
        category_id_value = 0

        # Act & Assert
        with pytest.raises(ValueError, match="カテゴリIDは正の整数である必要があります"):
            CategoryId(category_id_value)

    def test_init_with_negative_integer_raises_error(self):
        """異常系: 負の整数でCategoryIdを初期化するとValueErrorが発生する"""
        # Arrange
        category_id_value = -1

        # Act & Assert
        with pytest.raises(ValueError, match="カテゴリIDは正の整数である必要があります"):
            CategoryId(category_id_value)

    def test_init_with_negative_large_integer_raises_error(self):
        """異常系: 大きな負の整数でCategoryIdを初期化するとValueErrorが発生する"""
        # Arrange
        category_id_value = -999999999

        # Act & Assert
        with pytest.raises(ValueError, match="カテゴリIDは正の整数である必要があります"):
            CategoryId(category_id_value)

    def test_equality_with_same_value(self):
        """正常系: 同じ値を持つCategoryIdオブジェクトは等価である"""
        # Arrange
        category_id_value = 10
        category_id1 = CategoryId(category_id_value)
        category_id2 = CategoryId(category_id_value)

        # Act & Assert
        assert category_id1 == category_id2

    def test_equality_with_different_value(self):
        """正常系: 異なる値を持つCategoryIdオブジェクトは等価でない"""
        # Arrange
        category_id1 = CategoryId(1)
        category_id2 = CategoryId(2)

        # Act & Assert
        assert category_id1 != category_id2

    def test_equality_with_non_category_id_object(self):
        """正常系: CategoryIdオブジェクトと他の型のオブジェクトは等価でない"""
        # Arrange
        category_id = CategoryId(5)
        other_object = 5

        # Act & Assert
        assert category_id != other_object

    def test_hash_consistency(self):
        """正常系: 同じ値を持つCategoryIdオブジェクトは同じハッシュ値を持つ"""
        # Arrange
        category_id_value = 15
        category_id1 = CategoryId(category_id_value)
        category_id2 = CategoryId(category_id_value)

        # Act & Assert
        assert hash(category_id1) == hash(category_id2)

    def test_hash_different_for_different_values(self):
        """正常系: 異なる値を持つCategoryIdオブジェクトは異なるハッシュ値を持つ"""
        # Arrange
        category_id1 = CategoryId(1)
        category_id2 = CategoryId(2)

        # Act & Assert
        assert hash(category_id1) != hash(category_id2)

    def test_str_representation(self):
        """正常系: CategoryIdの文字列表現は値の文字列と同じである"""
        # Arrange
        category_id_value = 123
        category_id = CategoryId(category_id_value)

        # Act & Assert
        assert str(category_id) == str(category_id_value)
