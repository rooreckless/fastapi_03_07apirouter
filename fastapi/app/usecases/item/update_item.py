# ③ユースケース
# app/usecases/item/update_item.py
from app.domain.entities.item import Item
from app.repository.item_repository import ItemRepository

class UpdateItemUseCase:
    def __init__(self, repo: ItemRepository):
        # 引数のrepoの型は②抽象リポジトリクラス(=④リポジトリ実装のインターフェース)である。
        self.repo = repo

    async def execute(self, item_id: int, name: str, category_id: int) -> Item | None:
        # 更新対象のItemを取得(repoは②=④を継承しているのでいきなりget_by_idができる)
        item = await self.repo.get_by_id(item_id)
        if item is None:
            return None

        # 値を更新（エンティティ自体を更新）
        item.name = name
        item.category_id = category_id
        # 実際に更新するのは以下(④で内容は実装している(もっとも④では②を継承しているからupdateメソッドを作成せざるをえないのだが))
        await self.repo.update(item)
        return item
