# ③ユースケース
from app.repository.item_repository import ItemRepository
from app.domain.entities.item import Item

class GetItemUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, item_id: int) -> Item | None:
        return await self.repo.get_by_id(item_id)
