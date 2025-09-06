# Infrastructure層 - Repository実装
# SQLAlchemyを使用したItemリポジトリの具象実装
# 責務：
# - 抽象リポジトリインターフェースの実装
# - データベースへのCRUD操作
# - Mapperを使用したドメインエンティティとORMモデル間の変換
# - カテゴリとの多対多関係の管理
# - トランザクション管理

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.mappers.item_mapper import ItemMapper
from app.domain.items import Item
from app.abstract_repository.item_repository import ItemRepository  # 抽象リポジトリ


class SQLAlchemyItemRepository(ItemRepository):
    """SQLAlchemyを使用したItemリポジトリの具象実装クラス"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.mapper = ItemMapper()

    async def save(self, item: Item) -> None:
        """アイテムを保存する（新規作成または更新）
        
        Args:
            item: 保存するItemエンティティ
        """
        # CategoryORMインスタンスを取得(item.category_idsから該当するカテゴリを検索)
        categories = []
        if item.category_ids:
            result = await self.db.execute(
                select(CategoryORM).filter(
                    CategoryORM.category_id.in_(item.category_ids)
                )
            )
            categories = result.scalars().all()
        
        # Mapperを使用してドメインエンティティをORMモデルに変換
        orm = self.mapper.to_orm(item)
        # カテゴリの関連付けを設定
        orm.categories = categories
        
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        item.id = orm.item_id   # エンティティへIDを返す

    async def list_all(self) -> list[Item]:
        """全アイテムをリスト形式で取得
        
        Returns:
            list[Item]: アイテムエンティティのリスト
        """
        res = await self.db.execute(
            select(ItemORM).options(selectinload(ItemORM.categories))
        )
        return self.mapper.to_domain_list(res.scalars().all())

    async def get_by_id(self, item_id: int) -> Item | None:
        """IDによるアイテムの取得
        
        Args:
            item_id: 取得するアイテムのID
            
        Returns:
            Item | None: アイテムエンティティまたはNone
        """
        result = await self.db.execute(
            select(ItemORM)
            .options(selectinload(ItemORM.categories))
            .filter(ItemORM.item_id == item_id)
        )
        row = result.scalar_one_or_none()
        return self.mapper.to_domain(row) if row else None
    
    async def next_identifier(self) -> int:
        """アイテムのIDを生成するためのメソッド
        
        Returns:
            int: 新しいアイテムID
        """
        # 最新のID値(=itemテーブルの最大のid値)を持つレコードを取得
        result = await self.db.execute(
            select(ItemORM.item_id)
            .order_by(ItemORM.item_id.desc())
            .limit(1)
        )
        # そのレコードのID値を取得
        row = result.scalar_one_or_none()
        # もしレコードが存在しない場合は1を返す
        # 存在する場合はそのID値に1を足して返す
        return (row + 1) if row is not None else 1

    async def update(self, item: Item) -> None:
        """アイテムを更新する
        
        Args:
            item: 更新するItemエンティティ
        """
        # まず既存のアイテムを関係データと一緒に取得
        result = await self.db.execute(
            select(ItemORM)
            .options(selectinload(ItemORM.categories))
            .filter(ItemORM.item_id == item.id)
        )
        db_item = result.scalar_one_or_none()
         
        if db_item:
            db_item.item_name = item.name
            
            # カテゴリの更新処理
            if item.category_ids is not None and len(item.category_ids) > 0:
                # 新しいカテゴリを取得
                category_result = await self.db.execute(
                    select(CategoryORM).filter(
                        CategoryORM.category_id.in_(item.category_ids)
                    )
                )
                categories = list(category_result.scalars().all())
                db_item.categories = categories
                # エンティティの状態を更新
                item.category_ids = [cat.category_id for cat in categories]
            else:
                # category_idsがNoneまたは空リストの場合、すべてのカテゴリを削除
                db_item.categories = []
                # エンティティの状態を更新（一貫性のため空リストに統一）
                item.category_ids = []
            
            await self.db.commit()

    async def delete(self, item_id: int) -> Item | None:
        """アイテムを削除する
        
        Args:
            item_id: 削除するアイテムのID
            
        Returns:
            Item | None: 削除されたアイテムまたはNone
        """
        item = await self.db.get(ItemORM, item_id)
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found.")
        await self.db.delete(item)
        await self.db.commit()