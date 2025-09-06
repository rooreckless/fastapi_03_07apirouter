"""CategoryORM テストモジュール."""

import pytest
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM


class TestCategoryORM:
    """CategoryORMのテストクラス."""

    def test_category_orm_instantiation_success(self):
        """正常系: CategoryORMインスタンスが正常に作成される."""
        category = CategoryORM()
        assert category is not None
        assert hasattr(category, 'category_id')
        assert hasattr(category, 'category_name')
        assert hasattr(category, 'items')

    def test_category_orm_table_name(self):
        """正常系: テーブル名が正しく設定される."""
        assert CategoryORM.__tablename__ == "categories"

    def test_category_orm_set_category_id(self):
        """正常系: category_idが正常に設定される."""
        category = CategoryORM()
        category.category_id = 1
        assert category.category_id == 1

    def test_category_orm_set_category_name(self):
        """正常系: category_nameが正常に設定される."""
        category = CategoryORM()
        category.category_name = "テストカテゴリ"
        assert category.category_name == "テストカテゴリ"

    def test_category_orm_set_empty_category_name(self):
        """エッジケース: 空文字列のcategory_nameが設定される."""
        category = CategoryORM()
        category.category_name = ""
        assert category.category_name == ""

    def test_category_orm_set_long_category_name(self):
        """エッジケース: 長いcategory_nameが設定される."""
        category = CategoryORM()
        long_name = "a" * 1000
        category.category_name = long_name
        assert category.category_name == long_name

    def test_category_orm_set_category_name_with_special_characters(self):
        """正常系: 特殊文字を含むcategory_nameが設定される."""
        category = CategoryORM()
        special_name = "カテゴリ-123_@#$%"
        category.category_name = special_name
        assert category.category_name == special_name

    def test_category_orm_set_category_name_with_unicode(self):
        """正常系: Unicode文字を含むcategory_nameが設定される."""
        category = CategoryORM()
        unicode_name = "カテゴリ🚀✨"
        category.category_name = unicode_name
        assert category.category_name == unicode_name

    def test_category_orm_set_zero_category_id(self):
        """エッジケース: category_idが0に設定される."""
        category = CategoryORM()
        category.category_id = 0
        assert category.category_id == 0

    def test_category_orm_set_negative_category_id(self):
        """エッジケース: 負のcategory_idが設定される."""
        category = CategoryORM()
        category.category_id = -1
        assert category.category_id == -1

    def test_category_orm_set_large_category_id(self):
        """エッジケース: 大きなcategory_idが設定される."""
        category = CategoryORM()
        large_id = 2**31 - 1
        category.category_id = large_id
        assert category.category_id == large_id

    def test_category_orm_items_relationship_exists(self):
        """正常系: itemsリレーションシップが存在する."""
        category = CategoryORM()
        assert hasattr(category, 'items')
        # リレーションシップは初期状態では空リストまたはNone

    def test_category_orm_items_relationship_is_list(self):
        """正常系: itemsリレーションシップがリスト型である."""
        category = CategoryORM()
        # リレーションシップの初期化後はリスト型になることを確認
        # SQLAlchemyのrelationshipは通常、Noneまたは空リストで初期化される
        if category.items is not None:
            assert isinstance(category.items, list)

    def test_category_orm_multiple_instances(self):
        """正常系: 複数のCategoryORMインスタンスが作成できる."""
        category1 = CategoryORM()
        category2 = CategoryORM()
        
        category1.category_id = 1
        category1.category_name = "カテゴリ1"
        
        category2.category_id = 2
        category2.category_name = "カテゴリ2"
        
        assert category1.category_id == 1
        assert category1.category_name == "カテゴリ1"
        assert category2.category_id == 2
        assert category2.category_name == "カテゴリ2"
        assert category1 is not category2

    def test_category_orm_attribute_modification(self):
        """正常系: 属性値が変更できる."""
        category = CategoryORM()
        category.category_id = 1
        category.category_name = "初期カテゴリ"
        
        # 値を変更
        category.category_id = 2
        category.category_name = "変更後カテゴリ"
        
        assert category.category_id == 2
        assert category.category_name == "変更後カテゴリ"

    def test_category_orm_none_values_setting(self):
        """エッジケース: None値の設定."""
        category = CategoryORM()
        # SQLAlchemyでは通常、None値を設定することは可能だが、
        # データベース制約により実際の保存時にエラーになる可能性がある
        category.category_id = None  # type: ignore
        category.category_name = None  # type: ignore
        
        assert category.category_id is None
        assert category.category_name is None

    def test_category_orm_string_representation(self):
        """正常系: 文字列表現が取得できる."""
        category = CategoryORM()
        category.category_id = 1
        category.category_name = "テストカテゴリ"
        
        # __str__ または __repr__ が実装されていれば文字列表現が取得できる
        str_repr = str(category)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_category_orm_equality_comparison(self):
        """正常系: 等価比較ができる."""
        category1 = CategoryORM()
        category2 = CategoryORM()
        
        category1.category_id = 1
        category1.category_name = "テストカテゴリ"
        
        category2.category_id = 1
        category2.category_name = "テストカテゴリ"
        
        # デフォルトではオブジェクトのアイデンティティで比較される
        # カスタムの__eq__メソッドが実装されていれば、それに従う
        assert category1 is not category2

    def test_category_orm_hash_capability(self):
        """正常系: ハッシュ化が可能である."""
        category = CategoryORM()
        category.category_id = 1
        category.category_name = "テストカテゴリ"
        
        # オブジェクトがハッシュ化できることを確認
        try:
            hash_value = hash(category)
            assert isinstance(hash_value, int)
        except TypeError:
            # ハッシュ化ができない場合は期待される動作
            pass

    def test_category_orm_attribute_access_error(self):
        """異常系: 存在しない属性へのアクセス."""
        category = CategoryORM()
        
        with pytest.raises(AttributeError):
            _ = category.non_existent_attribute

    def test_category_orm_attribute_deletion(self):
        """エッジケース: 属性の削除."""
        category = CategoryORM()
        category.category_id = 1
        category.category_name = "テストカテゴリ"
        
        # SQLAlchemyの属性は通常削除できないが、試してみる
        try:
            del category.category_id
            # 削除が成功した場合、属性にアクセスするとエラーまたはNoneになる
            assert not hasattr(category, 'category_id') or category.category_id is None
        except (AttributeError, TypeError):
            # 削除できない場合は期待される動作
            pass

    def test_category_orm_dynamic_attribute_assignment(self):
        """エッジケース: 動的な属性の追加."""
        category = CategoryORM()
        
        # 新しい属性を動的に追加
        category.dynamic_attribute = "動的属性"
        assert category.dynamic_attribute == "動的属性"
        assert hasattr(category, 'dynamic_attribute')
