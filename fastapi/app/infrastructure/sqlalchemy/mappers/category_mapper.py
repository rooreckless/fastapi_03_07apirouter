# Infrastructure層 - Category Mapper
# CategoryORMとCategoryドメインエンティティ間の変換ロジックを担当
# 責務：
# - ORMモデル → ドメインエンティティへの変換
# - ドメインエンティティ → ORMモデルへの変換
# - リスト形式での一括変換

from app.domain.category import Category
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM

class CategoryMapper:
    """CategoryORMとCategoryドメインエンティティ間の変換を行うマッパークラス"""
    
    @staticmethod
    def to_domain(orm: CategoryORM) -> Category:
        """ORMモデルからドメインエンティティへの変換
        
        Args:
            orm: CategoryORMインスタンス
            
        Returns:
            Category: ドメインエンティティ
        """
        return Category(
            category_id=orm.category_id, 
            name=orm.category_name,
            created_by=orm.created_by,
            updated_by=orm.updated_by,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    @staticmethod
    def to_orm(category: Category) -> CategoryORM:
        """ドメインエンティティからORMモデルへの変換
        
        Args:
            category: Categoryドメインエンティティ
            
        Returns:
            CategoryORM: ORMモデルインスタンス
        """
        return CategoryORM(
            category_id=category.id, 
            category_name=category.name,
            created_by=category.created_by,
            updated_by=category.updated_by,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
    
    @staticmethod
    def to_domain_list(orm_list: list[CategoryORM]) -> list[Category]:
        """ORMモデルリストからドメインエンティティリストへの変換
        
        Args:
            orm_list: CategoryORMインスタンスのリスト
            
        Returns:
            list[Category]: ドメインエンティティのリスト
        """
        return [CategoryMapper.to_domain(orm) for orm in orm_list]
