# ③ユースケース
# app/usecases/category/list_categories.py

from app.domain.entities.category import Category
from app.repository.category_repository import CategoryRepository
class ListCategoriesUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self) -> list[Category]:
        return await self.repo.list_all()
