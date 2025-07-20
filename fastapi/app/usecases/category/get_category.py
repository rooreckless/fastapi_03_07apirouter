# ③ユースケース
from app.repository.category_repository import CategoryRepository
from app.domain.category import Category

class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, category_id: int) -> Category | None:
        return await self.repo.get_by_id(category_id)
