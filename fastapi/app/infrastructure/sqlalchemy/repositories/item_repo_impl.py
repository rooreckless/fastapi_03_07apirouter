# ④Infrastructure層 = 実装(具象)リポジトリ
# app/infrastructure/sqlalchemy/repositories/item_repo_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.domain.items import Item
from app.repository.item_repository import ItemRepository  # ②の抽象リポジトリ


class SQLAlchemyItemRepository(ItemRepository):
    # ②の抽象リポジトリを継承して実装
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, item: Item) -> None:
        # Itemの追加など保存時に使う
            
        # CategoryORMインスタンスを取得(item.category_idsで直接ItemORMを取得しない。いちいち、リストの長さ分CategoryORMを検索する)
        categories = []
        if item.category_ids:
            result = await self.db.execute(
                select(CategoryORM).filter(
                    CategoryORM.category_id.in_(item.category_ids)
                )
            )
            categories = result.scalars().all()
        
        orm = ItemORM(
            item_id=item.id,
            item_name=item.name,
            categories=categories
        )
        
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        item.id = orm.item_id   # ①のエンティティへIDを返す

    async def list_all(self) -> list[Item]:
        # Itemの一覧取得時に使う
        res = await self.db.execute(
            select(ItemORM).options(selectinload(ItemORM.categories))
        )
        items = []
        for r in res.scalars().all():
            category_ids = [cat.category_id for cat in r.categories]
            items.append(Item(r.item_id, r.item_name, category_ids))
        return items

    async def get_by_id(self, item_id: int) -> Item | None:
        # Itemの詳細取得に使う
        result = await self.db.execute(
            select(ItemORM)
            .options(selectinload(ItemORM.categories))
            .filter(ItemORM.item_id == item_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        category_ids = [cat.category_id for cat in row.categories]
        return Item(
            item_id=row.item_id,
            name=row.item_name,
            category_ids=category_ids
        )
    
    async def next_identifier(self) -> int:
        # アイテムのIDを生成するためのメソッド
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
        # Itemの更新に使う
        db_item = await self.db.get(ItemORM, item.id)
        if db_item:
            db_item.item_name = item.name
            
            # カテゴリの更新処理
            if item.category_ids:
                result = await self.db.execute(
                    select(CategoryORM).filter(
                        CategoryORM.category_id.in_(item.category_ids)
                    )
                )
                categories = result.scalars().all()
                db_item.categories = categories
            else:
                db_item.categories = []
                
            await self.db.commit()

    async def delete(self, item_id: int) -> Item | None:
        # Itemの削除に使う
        item = await self.db.get(ItemORM, item_id)
        print("----item=", item)
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found.")
        await self.db.delete(item)
        await self.db.commit()