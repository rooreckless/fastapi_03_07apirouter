# ④Infrastructure層 = 実装(具象)リポジトリ
# app/infrastructure/sqlalchemy/repositories/item_repo_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.domain.entities.item import Item
from app.repository.item_repository import ItemRepository  # ②の抽象リポジトリ


class SQLAlchemyItemRepository(ItemRepository):
    #  ②の抽象リポジトリを継承して実装
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, item: Item) -> None:
        # Itemの追加など保存時に使う
        orm = ItemORM(item_name=item.name, category_id=item.category_id)
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        item.id = orm.item_id   # ①のエンティティへIDを返す

    async def list_all(self) -> list[Item]:
        # Itemの一覧取得時に使う
        res = await self.db.execute(select(ItemORM))
        return [Item(r.item_id, r.item_name, r.category_id) for r in res.scalars().all()]

    async def get_by_id(self, item_id: int) -> Item | None:
        # Itemの詳細取得に使う
        result = await self.db.execute(
            select(ItemORM).filter(ItemORM.item_id == item_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return Item(item_id=row.item_id, name=row.item_name, category_id=row.category_id)