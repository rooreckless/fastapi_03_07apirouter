"""
item.pyのテストモジュール
"""

from app.domain.items.item import Item


class TestItem:
    """Itemクラスのテストクラス"""

    def test_init_with_all_parameters(self):
        """正常系: すべてのパラメータを指定してItemを初期化する"""
        # Arrange
        item_id = 1
        name = "テストアイテム"
        category_ids = [1, 2, 3]

        # Act
        item = Item(item_id=item_id, name=name, category_ids=category_ids)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids == category_ids

    def test_init_with_none_category_ids(self):
        """正常系: category_idsをNoneでItemを初期化する"""
        # Arrange
        item_id = 1
        name = "テストアイテム"

        # Act
        item = Item(item_id=item_id, name=name, category_ids=None)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids is None

    def test_init_without_category_ids(self):
        """正常系: category_idsを省略してItemを初期化する（デフォルト値None）"""
        # Arrange
        item_id = 1
        name = "テストアイテム"

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids is None

    def test_init_with_empty_category_ids(self):
        """エッジケース: category_idsに空のリストを指定してItemを初期化する"""
        # Arrange
        item_id = 1
        name = "テストアイテム"
        category_ids = []

        # Act
        item = Item(item_id=item_id, name=name, category_ids=category_ids)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids == []

    def test_init_with_zero_item_id(self):
        """エッジケース: item_idに0を指定してItemを初期化する"""
        # Arrange
        item_id = 0
        name = "テストアイテム"

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == 0
        assert item.name == name
        assert item.category_ids is None

    def test_init_with_negative_item_id(self):
        """エッジケース: item_idに負の値を指定してItemを初期化する"""
        # Arrange
        item_id = -1
        name = "テストアイテム"

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == -1
        assert item.name == name
        assert item.category_ids is None

    def test_init_with_empty_string_name(self):
        """エッジケース: nameに空文字列を指定してItemを初期化する"""
        # Arrange
        item_id = 1
        name = ""

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == item_id
        assert item.name == ""
        assert item.category_ids is None

    def test_init_with_single_category_id(self):
        """正常系: category_idsに単一の要素を持つリストを指定してItemを初期化する"""
        # Arrange
        item_id = 1
        name = "テストアイテム"
        category_ids = [5]

        # Act
        item = Item(item_id=item_id, name=name, category_ids=category_ids)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids == [5]

    def test_init_with_large_item_id(self):
        """エッジケース: item_idに大きな値を指定してItemを初期化する"""
        # Arrange
        item_id = 999999999
        name = "テストアイテム"

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == 999999999
        assert item.name == name
        assert item.category_ids is None

    def test_init_with_long_name(self):
        """エッジケース: nameに長い文字列を指定してItemを初期化する"""
        # Arrange
        item_id = 1
        name = "a" * 1000  # 1000文字の文字列

        # Act
        item = Item(item_id=item_id, name=name)

        # Assert
        assert item.id == item_id
        assert item.name == name
        assert item.category_ids is None
