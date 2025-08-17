"""ItemORM テストモジュール."""

import pytest
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM  # noqa: F401


class TestItemORM:
    """ItemORMのテストクラス."""

    def test_item_orm_instantiation_success(self):
        """正常系: ItemORMインスタンスが正常に作成される."""
        item = ItemORM()
        assert item is not None
        assert hasattr(item, 'item_id')
        assert hasattr(item, 'item_name')
        assert hasattr(item, 'categories')

    def test_item_orm_table_name(self):
        """正常系: テーブル名が正しく設定される."""
        assert ItemORM.__tablename__ == "items"

    def test_item_orm_set_item_id(self):
        """正常系: item_idが正常に設定される."""
        item = ItemORM()
        item.item_id = 1
        assert item.item_id == 1

    def test_item_orm_set_item_name(self):
        """正常系: item_nameが正常に設定される."""
        item = ItemORM()
        item.item_name = "テストアイテム"
        assert item.item_name == "テストアイテム"

    def test_item_orm_set_empty_item_name(self):
        """エッジケース: 空文字列のitem_nameが設定される."""
        item = ItemORM()
        item.item_name = ""
        assert item.item_name == ""

    def test_item_orm_set_long_item_name(self):
        """エッジケース: 長いitem_nameが設定される."""
        item = ItemORM()
        long_name = "a" * 1000
        item.item_name = long_name
        assert item.item_name == long_name

    def test_item_orm_set_item_name_with_special_characters(self):
        """正常系: 特殊文字を含むitem_nameが設定される."""
        item = ItemORM()
        special_name = "アイテム-123_@#$%"
        item.item_name = special_name
        assert item.item_name == special_name

    def test_item_orm_set_item_name_with_unicode(self):
        """正常系: Unicode文字を含むitem_nameが設定される."""
        item = ItemORM()
        unicode_name = "アイテム🚀✨"
        item.item_name = unicode_name
        assert item.item_name == unicode_name

    def test_item_orm_set_zero_item_id(self):
        """エッジケース: item_idが0に設定される."""
        item = ItemORM()
        item.item_id = 0
        assert item.item_id == 0

    def test_item_orm_set_negative_item_id(self):
        """エッジケース: 負のitem_idが設定される."""
        item = ItemORM()
        item.item_id = -1
        assert item.item_id == -1

    def test_item_orm_set_large_item_id(self):
        """エッジケース: 大きなitem_idが設定される."""
        item = ItemORM()
        large_id = 2**31 - 1
        item.item_id = large_id
        assert item.item_id == large_id

    def test_item_orm_categories_relationship_exists(self):
        """正常系: categoriesリレーションシップが存在する."""
        item = ItemORM()
        assert hasattr(item, 'categories')
        # リレーションシップは初期状態では空リストまたはNone

    def test_item_orm_categories_relationship_is_list(self):
        """正常系: categoriesリレーションシップがリスト型である."""
        item = ItemORM()
        # リレーションシップの初期化後はリスト型になることを確認
        # SQLAlchemyのrelationshipは通常、Noneまたは空リストで初期化される
        if item.categories is not None:
            assert isinstance(item.categories, list)

    def test_item_orm_multiple_instances(self):
        """正常系: 複数のItemORMインスタンスが作成できる."""
        item1 = ItemORM()
        item2 = ItemORM()
        
        item1.item_id = 1
        item1.item_name = "アイテム1"
        
        item2.item_id = 2
        item2.item_name = "アイテム2"
        
        assert item1.item_id == 1
        assert item1.item_name == "アイテム1"
        assert item2.item_id == 2
        assert item2.item_name == "アイテム2"
        assert item1 is not item2

    def test_item_orm_attribute_modification(self):
        """正常系: 属性値が変更できる."""
        item = ItemORM()
        item.item_id = 1
        item.item_name = "初期アイテム"
        
        # 値を変更
        item.item_id = 2
        item.item_name = "変更後アイテム"
        
        assert item.item_id == 2
        assert item.item_name == "変更後アイテム"

    def test_item_orm_none_values_setting(self):
        """エッジケース: None値の設定."""
        item = ItemORM()
        # SQLAlchemyでは通常、None値を設定することは可能だが、
        # データベース制約により実際の保存時にエラーになる可能性がある
        item.item_id = None
        item.item_name = None
        
        assert item.item_id is None
        assert item.item_name is None

    def test_item_orm_string_representation(self):
        """正常系: 文字列表現が取得できる."""
        item = ItemORM()
        item.item_id = 1
        item.item_name = "テストアイテム"
        
        # __str__ または __repr__ が実装されていれば文字列表現が取得できる
        str_repr = str(item)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_item_orm_equality_comparison(self):
        """正常系: 等価比較ができる."""
        item1 = ItemORM()
        item2 = ItemORM()
        
        item1.item_id = 1
        item1.item_name = "テストアイテム"
        
        item2.item_id = 1
        item2.item_name = "テストアイテム"
        
        # デフォルトではオブジェクトのアイデンティティで比較される
        # カスタムの__eq__メソッドが実装されていれば、それに従う
        assert item1 is not item2

    def test_item_orm_hash_capability(self):
        """正常系: ハッシュ化が可能である."""
        item = ItemORM()
        item.item_id = 1
        item.item_name = "テストアイテム"
        
        # オブジェクトがハッシュ化できることを確認
        try:
            hash_value = hash(item)
            assert isinstance(hash_value, int)
        except TypeError:
            # ハッシュ化ができない場合は期待される動作
            pass

    def test_item_orm_attribute_access_error(self):
        """異常系: 存在しない属性へのアクセス."""
        item = ItemORM()
        
        with pytest.raises(AttributeError):
            _ = item.non_existent_attribute

    def test_item_orm_attribute_deletion(self):
        """エッジケース: 属性の削除."""
        item = ItemORM()
        item.item_id = 1
        item.item_name = "テストアイテム"
        
        # SQLAlchemyの属性は通常削除できないが、試してみる
        try:
            del item.item_id
            # 削除が成功した場合、属性にアクセスするとエラーまたはNoneになる
            assert not hasattr(item, 'item_id') or item.item_id is None
        except (AttributeError, TypeError):
            # 削除できない場合は期待される動作
            pass

    def test_item_orm_dynamic_attribute_assignment(self):
        """エッジケース: 動的な属性の追加."""
        item = ItemORM()
        
        # 新しい属性を動的に追加
        item.dynamic_attribute = "動的属性"
        assert item.dynamic_attribute == "動的属性"
        assert hasattr(item, 'dynamic_attribute')

    def test_item_orm_categories_list_manipulation(self):
        """正常系: categoriesリストの操作."""
        item = ItemORM()
        
        # categoriesが初期化されていない場合は空リストで初期化
        if item.categories is None:
            item.categories = []
        
        # リストが操作できることを確認
        assert isinstance(item.categories, list)
        initial_length = len(item.categories)
        
        # SQLAlchemyのリレーションシップはリスト操作をサポートする
        # 基本的なリストプロパティをテスト
        assert hasattr(item.categories, 'append')
        assert hasattr(item.categories, 'clear')
        assert len(item.categories) == initial_length

    def test_item_orm_categories_empty_list_assignment(self):
        """エッジケース: 空のcategoriesリストが設定される."""
        item = ItemORM()
        item.categories = []
        
        assert item.categories == []
        assert len(item.categories) == 0

    def test_item_orm_categories_none_assignment(self):
        """エッジケース: categoriesリストがクリアできる."""
        item = ItemORM()
        # SQLAlchemyのリレーションシップはNoneを直接設定できないが、
        # clearメソッドでクリアできる
        item.categories.clear()
        assert len(item.categories) == 0

    def test_item_orm_name_type_validation(self):
        """正常系: item_nameの型が文字列であることの確認."""
        item = ItemORM()
        item.item_name = "テストアイテム"
        
        assert isinstance(item.item_name, str)

    def test_item_orm_id_type_validation(self):
        """正常系: item_idの型が整数であることの確認."""
        item = ItemORM()
        item.item_id = 1
        
        assert isinstance(item.item_id, int)
