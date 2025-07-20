# ③ユースケース
# app/usecases/category/create_category.py
from app.domain.category import Category
from app.repository.category_repository import CategoryRepository

class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, name: str) -> Category:
        # 新しいカテゴリを作成する前に、次のIDを取得
        new_category_id = await self.repo.next_identifier()
        # 次にカテゴリモデル(=エンティティ)からカテゴリを作成
        category = Category(category_id=new_category_id, name=name)
        # 作成したカテゴリをリポジトリに保存
        await self.repo.save(category)
        return category
