# ④Infrastructure層 = 実装(具象)リポジトリ
# app/infrastructure/sqlalchemy/repositories/category_repo_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.domain.entities.category import Category
from app.repository.category_repository import CategoryRepository # ②の抽象リポジトリ

class SQLAlchemyCategoryRepository(CategoryRepository):
    #  ②の抽象リポジトリを継承して実装
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, category: Category) -> None:
        orm = CategoryORM(category_name=category.name)
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        category.id = orm.category_id   # ①のエンティティへIDを返す

    async def list_all(self) -> list[Category]:
        res = await self.db.execute(select(CategoryORM))
        return [Category(r.category_id, r.category_name) for r in res.scalars().all()]
