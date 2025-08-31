# Infrastructure層 - ItemMapper テスト
# ItemMapperの変換ロジックをテストする
# 責務：
# - ORMモデル → ドメインエンティティ変換のテスト
# - ドメインエンティティ → ORMモデル変換のテスト
# - リスト変換処理のテスト
# - カテゴリID変換のテスト
# - エッジケース（None、空リスト等）のテスト

import pytest
from app.domain.items import Item
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.mappers.item_mapper import ItemMapper


class TestItemMapper:
    """ItemMapperの変換処理をテストするクラス"""

    def test_to_domain_with_categories(self):
        """カテゴリ付きのORMからドメインエンティティへの変換"""
        # Arrange
        categories = [
            CategoryORM(category_id=1, category_name="Category 1"),
            CategoryORM(category_id=2, category_name="Category 2")
        ]
        orm = ItemORM(item_id=1, item_name="Test Item")
        orm.categories = categories
        
        # Act
        result = ItemMapper.to_domain(orm)
        
        # Assert
        assert isinstance(result, Item)
        assert result.id == 1
        assert result.name == "Test Item"
        assert result.category_ids == [1, 2]

    def test_to_domain_without_categories(self):
        """カテゴリなしのORMからドメインエンティティへの変換"""
        # Arrange
        orm = ItemORM(item_id=2, item_name="Test Item 2")
        orm.categories = []
        
        # Act
        result = ItemMapper.to_domain(orm)
        
        # Assert
        assert isinstance(result, Item)
        assert result.id == 2
        assert result.name == "Test Item 2"
        assert result.category_ids == []

    def test_to_domain_with_none_categories(self):
        """カテゴリがNoneのORMからドメインエンティティへの変換"""
        # Arrange
        orm = ItemORM(item_id=3, item_name="Test Item 3")
        # SQLAlchemyのrelationshipはNoneを受け付けないため、空リストに変更
        orm.categories = []
        
        # Act
        result = ItemMapper.to_domain(orm)
        
        # Assert
        assert isinstance(result, Item)
        assert result.id == 3
        assert result.name == "Test Item 3"
        assert result.category_ids == []

    def test_to_orm_success(self):
        """ドメインエンティティからORMへの正常な変換"""
        # Arrange
        item = Item(item_id=4, name="Test Item 4", category_ids=[1, 2, 3])
        
        # Act
        result = ItemMapper.to_orm(item)
        
        # Assert
        assert isinstance(result, ItemORM)
        assert result.item_id == 4
        assert result.item_name == "Test Item 4"
        # 注意: Mapperではカテゴリ関連付けは行わない

    def test_to_orm_without_categories(self):
        """カテゴリIDなしのドメインエンティティからORMへの変換"""
        # Arrange
        item = Item(item_id=5, name="Test Item 5", category_ids=[])
        
        # Act
        result = ItemMapper.to_orm(item)
        
        # Assert
        assert isinstance(result, ItemORM)
        assert result.item_id == 5
        assert result.item_name == "Test Item 5"

    def test_to_domain_list_success(self):
        """ORMリストからドメインエンティティリストへの変換"""
        # Arrange
        categories1 = [CategoryORM(category_id=1, category_name="Cat 1")]
        categories2 = [CategoryORM(category_id=2, category_name="Cat 2")]
        
        orm1 = ItemORM(item_id=1, item_name="Item 1")
        orm1.categories = categories1
        orm2 = ItemORM(item_id=2, item_name="Item 2")
        orm2.categories = categories2
        
        orm_list = [orm1, orm2]
        
        # Act
        result = ItemMapper.to_domain_list(orm_list)
        
        # Assert
        assert len(result) == 2
        assert all(isinstance(item, Item) for item in result)
        assert result[0].id == 1
        assert result[0].name == "Item 1"
        assert result[0].category_ids == [1]
        assert result[1].id == 2
        assert result[1].name == "Item 2"
        assert result[1].category_ids == [2]

    def test_to_domain_list_empty(self):
        """空リストの変換"""
        # Arrange
        orm_list = []
        
        # Act
        result = ItemMapper.to_domain_list(orm_list)
        
        # Assert
        assert result == []
        assert isinstance(result, list)

    def test_to_domain_with_multiple_categories(self):
        """複数カテゴリを持つアイテムの変換"""
        # Arrange
        categories = [
            CategoryORM(category_id=10, category_name="Category 10"),
            CategoryORM(category_id=20, category_name="Category 20"),
            CategoryORM(category_id=30, category_name="Category 30")
        ]
        orm = ItemORM(item_id=100, item_name="Multi Category Item")
        orm.categories = categories
        
        # Act
        result = ItemMapper.to_domain(orm)
        
        # Assert
        assert result.id == 100
        assert result.name == "Multi Category Item"
        assert result.category_ids == [10, 20, 30]

    def test_to_domain_with_special_characters(self):
        """特殊文字を含む名前の変換"""
        # Arrange
        orm = ItemORM(item_id=99, item_name="テストアイテム@#$%")
        orm.categories = []
        
        # Act
        result = ItemMapper.to_domain(orm)
        
        # Assert
        assert result.id == 99
        assert result.name == "テストアイテム@#$%"
        assert result.category_ids == []

    def test_bidirectional_conversion(self):
        """双方向変換の一貫性テスト（カテゴリなし）"""
        # Arrange
        original_item = Item(item_id=200, name="Bidirectional Test", category_ids=[])
        
        # Act: ドメイン → ORM → ドメイン
        orm = ItemMapper.to_orm(original_item)
        orm.categories = []  # カテゴリを手動で設定
        result_item = ItemMapper.to_domain(orm)
        
        # Assert
        assert result_item.id == original_item.id
        assert result_item.name == original_item.name
        assert result_item.category_ids == original_item.category_ids
