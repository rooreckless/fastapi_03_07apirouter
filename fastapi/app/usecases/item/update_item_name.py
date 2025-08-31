# ③ユースケース
# app/usecases/item/update_item_name.py
from app.abstract_repository.item_repository import ItemRepository
from app.domain.items import Item

class UpdateItemNameUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, item_id: int, new_name: str, updated_by_user_id: int) -> Item:
        item = await self.repo.get_by_id(item_id)
        if item is None:
            raise ValueError("Item not found")

        item.name = new_name
        item.updated_by = updated_by_user_id
        await self.repo.update(item)
        
        # 更新後、データベースから最新の情報（updated_atを含む）を取得
        updated_item = await self.repo.get_by_id(item_id)
        return updated_item if updated_item else item
