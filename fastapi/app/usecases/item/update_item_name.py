# ③ユースケース
# app/usecases/item/update_item_name.py
from app.repository.item_repository import ItemRepository
from app.domain.items import Item

class UpdateItemNameUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, item_id: int, new_name: str) -> Item:
        item = await self.repo.get_by_id(item_id)
        if item is None:
            raise ValueError("Item not found")

        item.name = new_name
        await self.repo.update(item)
        return item
