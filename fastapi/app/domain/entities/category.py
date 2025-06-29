# ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/entities/category.py
class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name
