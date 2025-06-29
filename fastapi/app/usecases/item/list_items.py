# ③ユースケース
# app/usecases/item/list_items
from app.domain.entities.item import Item
from app.repository.item_repository import ItemRepository
class ListItemsUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self) -> list[Item]:
        return await self.repo.list_all()