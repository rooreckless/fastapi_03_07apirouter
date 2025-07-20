# ③ユースケース
# app/usecases/item/create_item.py
from app.domain.items import Item
from app.repository.item_repository import ItemRepository

class CreateItemUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, name: str, category_id: int) -> Item:

        print("---usecase---name=",name,"category_id=",category_id)
        item = Item(item_id=0, name=name, category_id=category_id)
        await self.repo.save(item)
        return item
