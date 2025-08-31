# ③ユースケース
# app/usecases/category/create_category.py
from app.domain.category.entity.category import Category
from app.abstract_repository.category_repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, name: str, created_by_user_id: int) -> Category:
        # 新しいカテゴリを作成する前に、次のIDを取得
        new_category_id = await self.repo.next_identifier()
        # 次にカテゴリモデル(=エンティティ)からカテゴリを作成
        category = Category(
            category_id=new_category_id, 
            name=name,
            created_by=created_by_user_id,
            updated_by=created_by_user_id
        )
        # 作成したカテゴリをリポジトリに保存
        await self.repo.save(category)
        
        # 保存後、データベースから最新の情報（created_at, updated_atを含む）を取得
        saved_category = await self.repo.get_by_id(new_category_id)
        return saved_category if saved_category else category
