# ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/entities/item.py
class Item:
    def __init__(self, item_id: int, name: str, category_id: int):
        self.id = item_id
        self.name = name
        self.category_id = category_id
