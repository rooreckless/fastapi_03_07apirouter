# ③ユースケース
from app.repository.item_repository import ItemRepository
from app.domain.entities.item import Item

class DeleteItemUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, item_id: int) -> Item | None:
        await self.repo.delete(item_id)
        return None