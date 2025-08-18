# ①ドメイン層 (旧形式ではmodelsディレクトリ内に似ているが違う。ここは業務ルールが入る)
# app/domain/category/category.py
class Category:
    def __init__(self, category_id: int, name: str):
        if category_id < 0:
            raise ValueError("カテゴリIDは0以上でなければなりません")
        self.id = category_id
        self.name = name
