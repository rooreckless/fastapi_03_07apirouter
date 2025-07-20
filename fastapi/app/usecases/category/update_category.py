# ③ユースケース
# app/usecases/category/update_category.py
from app.domain.category import Category
from app.repository.category_repository import CategoryRepository

class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        # 引数のrepoの型は②抽象リポジトリクラス(=④リポジトリ実装のインターフェース)である。
        self.repo = repo

    async def execute(self, category_id: int, name: str) -> Category | None:
        # 更新対象のCategoryを取得(repoは②=④を継承しているのでいきなりget_by_idができる)
        category = await self.repo.get_by_id(category_id)
        if category is None:
            return None

        # 値を更新（エンティティ自体を更新）
        category.name = name
        
        # 実際に更新するのは以下(④で内容は実装している(もっとも④では②を継承しているからupdateメソッドを作成せざるをえないのだが))
        await self.repo.update(category)
        return category
