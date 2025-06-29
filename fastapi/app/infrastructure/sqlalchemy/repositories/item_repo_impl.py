# app/infrastructure/sqlalchemy/repositories/item_repo_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.domain.entities.item import Item
from app.repository.item_repository import ItemRepository

class SQLAlchemyItemRepository(ItemRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, item: Item) -> None:
        orm = ItemORM(item_name=item.name, category_id=item.category_id)
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        item.id = orm.item_id   # エンティティへIDを返す

    async def list_all(self) -> list[Item]:
        res = await self.db.execute(select(ItemORM))
        return [Item(r.item_id, r.item_name, r.category_id) for r in res.scalars().all()]
