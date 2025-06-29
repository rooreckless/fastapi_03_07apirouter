# ③ユースケース
# app/usecases/category/create_category.py
from app.domain.entities.category import Category
from app.repository.category_repository import CategoryRepository

class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, name: str) -> Category:
        category = Category(category_id=0, name=name)
        await self.repo.save(category)
        return category
