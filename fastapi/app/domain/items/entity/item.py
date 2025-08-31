# ①ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/items/entity/item.py
class Item:
    def __init__(self, item_id: int, name: str, category_ids: list[int] | None = None):
        self.id = item_id
        self.name = name
        self.category_ids = category_ids
