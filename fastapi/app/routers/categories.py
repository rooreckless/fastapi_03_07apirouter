# routersディレクトリは、各種エンドポイントをグループ化して管理するフォルダです。
# 特定の機能やリソースに対するルート(urlパス)とビジネスロジックの処理を定義して配置します。
# 例えば、カテゴリ関連の操作をcategories.py,商品関連の操作をitems.pyとしてわけて管理できます。

from fastapi import APIRouter
from app.schemas.category import Category

router =APIRouter()

#---カテゴリ関連のルート---

@router.get("/categories/", response_model=dict)
async def read_categories():
    # 実際にはDBから取得処理がここ
    return {"message": "カテゴリ一覧を表示", "categories":[]}

@router.post("/categories/", response_model=dict)
async def create_category(category: Category):
    # 実際にはDBに保存する処理がここ
    return {"message": "カテゴリを作成", "category": category}

@router.put("/categories/{category_id}", response_model=dict)
async def update_category(category_id: int, category: Category):
    # 実際にはDBに更新する処理がここ
    return {"message": "カテゴリを更新", "category_id": category_id, "category": category}

@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: int):
    # 実際にはDBから削除する処理がここ
    return {"message": "カテゴリを削除", "category_id": category_id}