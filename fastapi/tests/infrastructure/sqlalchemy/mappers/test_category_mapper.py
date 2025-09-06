# Infrastructure層 - CategoryMapper テスト
# CategoryMapperの変換ロジックをテストする
# 責務：
# - ORMモデル → ドメインエンティティ変換のテスト
# - ドメインエンティティ → ORMモデル変換のテスト
# - リスト変換処理のテスト
# - エッジケース（None、空リスト等）のテスト

import pytest
from app.domain.category import Category
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.mappers.category_mapper import CategoryMapper


class TestCategoryMapper:
    """CategoryMapperの変換処理をテストするクラス"""

    def test_to_domain_success(self):
        """ORMからドメインエンティティへの正常な変換"""
        # Arrange
        orm = CategoryORM(category_id=1, category_name="Test Category")
        
        # Act
        result = CategoryMapper.to_domain(orm)
        
        # Assert
        assert isinstance(result, Category)
        assert result.id == 1
        assert result.name == "Test Category"

    def test_to_orm_success(self):
        """ドメインエンティティからORMへの正常な変換"""
        # Arrange
        category = Category(category_id=2, name="Test Category 2")
        
        # Act
        result = CategoryMapper.to_orm(category)
        
        # Assert
        assert isinstance(result, CategoryORM)
        assert result.category_id == 2
        assert result.category_name == "Test Category 2"

    def test_to_domain_list_success(self):
        """ORMリストからドメインエンティティリストへの正常な変換"""
        # Arrange
        orm_list = [
            CategoryORM(category_id=1, category_name="Category 1"),
            CategoryORM(category_id=2, category_name="Category 2"),
            CategoryORM(category_id=3, category_name="Category 3")
        ]
        
        # Act
        result = CategoryMapper.to_domain_list(orm_list)
        
        # Assert
        assert len(result) == 3
        assert all(isinstance(item, Category) for item in result)
        assert result[0].id == 1
        assert result[0].name == "Category 1"
        assert result[1].id == 2
        assert result[1].name == "Category 2"
        assert result[2].id == 3
        assert result[2].name == "Category 3"

    def test_to_domain_list_empty(self):
        """空リストの変換"""
        # Arrange
        orm_list = []
        
        # Act
        result = CategoryMapper.to_domain_list(orm_list)
        
        # Assert
        assert result == []
        assert isinstance(result, list)

    def test_to_domain_with_special_characters(self):
        """特殊文字を含む名前の変換"""
        # Arrange
        orm = CategoryORM(category_id=10, category_name="テストカテゴリ@#$%")
        
        # Act
        result = CategoryMapper.to_domain(orm)
        
        # Assert
        assert result.id == 10
        assert result.name == "テストカテゴリ@#$%"

    def test_to_orm_with_special_characters(self):
        """特殊文字を含む名前のORM変換"""
        # Arrange
        category = Category(category_id=11, name="スペシャル文字&()!")
        
        # Act
        result = CategoryMapper.to_orm(category)
        
        # Assert
        assert result.category_id == 11
        assert result.category_name == "スペシャル文字&()!"

    def test_to_domain_with_zero_id(self):
        """IDが0の場合の変換"""
        # Arrange
        orm = CategoryORM(category_id=0, category_name="Zero ID Category")
        
        # Act
        result = CategoryMapper.to_domain(orm)
        
        # Assert
        assert result.id == 0
        assert result.name == "Zero ID Category"

    def test_to_domain_with_large_id(self):
        """大きなIDの場合の変換"""
        # Arrange
        orm = CategoryORM(category_id=999999, category_name="Large ID Category")
        
        # Act
        result = CategoryMapper.to_domain(orm)
        
        # Assert
        assert result.id == 999999
        assert result.name == "Large ID Category"

    def test_to_domain_with_empty_name(self):
        """空の名前の場合の変換"""
        # Arrange
        orm = CategoryORM(category_id=5, category_name="")
        
        # Act
        result = CategoryMapper.to_domain(orm)
        
        # Assert
        assert result.id == 5
        assert result.name == ""

    def test_bidirectional_conversion(self):
        """双方向変換の一貫性テスト"""
        # Arrange
        original_category = Category(category_id=100, name="Bidirectional Test")
        
        # Act: ドメイン → ORM → ドメイン
        orm = CategoryMapper.to_orm(original_category)
        result_category = CategoryMapper.to_domain(orm)
        
        # Assert
        assert result_category.id == original_category.id
        assert result_category.name == original_category.name
