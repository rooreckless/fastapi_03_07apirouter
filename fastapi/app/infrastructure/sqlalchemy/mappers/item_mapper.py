# Infrastructure層 - Item Mapper
# ItemORMとItemドメインエンティティ間の変換ロジックを担当
# 責務：
# - ORMモデル → ドメインエンティティへの変換
# - ドメインエンティティ → ORMモデルへの変換
# - リスト形式での一括変換
# - カテゴリIDのリスト変換処理

from app.domain.items import Item
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM

class ItemMapper:
    """ItemORMとItemドメインエンティティ間の変換を行うマッパークラス"""
    
    @staticmethod
    def to_domain(orm: ItemORM) -> Item:
        """ORMモデルからドメインエンティティへの変換
        
        Args:
            orm: ItemORMインスタンス
            
        Returns:
            Item: ドメインエンティティ
        """
        # カテゴリIDのリストを作成（関連するCategoryORMからIDを抽出）
        category_ids = [category.category_id for category in orm.categories] if orm.categories else []
        
        return Item(
            item_id=orm.item_id,
            name=orm.item_name,
            category_ids=category_ids
        )
    
    @staticmethod
    def to_orm(item: Item) -> ItemORM:
        """ドメインエンティティからORMモデルへの変換
        
        Args:
            item: Itemドメインエンティティ
            
        Returns:
            ItemORM: ORMモデルインスタンス
        """
        # 注意: この時点ではカテゴリの関連付けは行わない
        # カテゴリの関連付けはリポジトリ層で別途処理する
        return ItemORM(
            item_id=item.id,
            item_name=item.name
        )
    
    @staticmethod
    def to_domain_list(orm_list: list[ItemORM]) -> list[Item]:
        """ORMモデルリストからドメインエンティティリストへの変換
        
        Args:
            orm_list: ItemORMインスタンスのリスト
            
        Returns:
            list[Item]: ドメインエンティティのリスト
        """
        return [ItemMapper.to_domain(orm) for orm in orm_list]
