# ③ユースケース
# app/usecases/item/create_item.py
from app.domain.items import Item
from app.abstract_repository.item_repository import ItemRepository

class CreateItemUseCase:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def execute(self, name: str, category_ids: list[int], created_by_user_id: int) -> Item:
        # 新しいアイテムを作成する前に、次のIDを取得
        new_item_id = await self.repo.next_identifier()
        # 次にアイテムモデル(=エンティティ)からアイテムを作成
        item = Item(
            item_id=new_item_id, 
            name=name, 
            category_ids=category_ids,
            created_by=created_by_user_id,
            updated_by=created_by_user_id
        )
        # 作成したアイテムをリポジトリに保存
        await self.repo.save(item)
        
        # 保存後、データベースから最新の情報（created_at, updated_atを含む）を取得
        saved_item = await self.repo.get_by_id(new_item_id)
        return saved_item if saved_item else item
