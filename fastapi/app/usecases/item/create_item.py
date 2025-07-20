# ③ユースケース
# app/usecases/item/create_item.py
from app.domain.items import Item
from app.repository.item_repository import ItemRepository

class CreateItemUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, name: str, category_ids: list[int]) -> Item:
        # 新しいアイテムを作成する前に、次のIDを取得
        new_item_id = await self.repo.next_identifier()
        # 次にアイテムモデル(=エンティティ)からアイテムを作成
        item = Item(item_id=new_item_id, name=name, category_ids=category_ids)
        # 作成したアイテムをリポジトリに保存
        await self.repo.save(item)
        return item
