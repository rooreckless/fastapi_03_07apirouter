from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}

#--- スキーマ---

class Category(BaseModel):
    category_id: int
    category_name: str
class Item(BaseModel):
    item_id: int
    item_name: str
    category_id: int

#---ルート----
#------カテゴリ------

@app.get("/categories/", response_model=dict)
async def read_categories():
    # 実際にはDBから取得処理がここ
    return {"message": "カテゴリ一覧を表示", "categories":[]}

@app.post("/categories/", response_model=dict)
async def create_category(category: Category):
    # 実際にはDBに保存する処理がここ
    return {"message": "カテゴリを作成", "category": category}

@app.put("/categories/{category_id}", response_model=dict)
async def update_category(category_id: int, category: Category):
    # 実際にはDBに更新する処理がここ
    return {"message": "カテゴリを更新", "category_id": category_id, "category": category}

@app.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: int):
    # 実際にはDBから削除する処理がここ
    return {"message": "カテゴリを削除", "category_id": category_id}

#------商品------

@app.get("/items/", response_model=dict)
async def read_items():
    # 実際にはDBから取得処理がここ
    return {"message": "商品一覧を表示", "items":[]}

@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    # 実際にはDBに保存する処理がここ
    return {"message": "商品を作成", "item": item}

@app.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, item: Item):
    # 実際にはDBに更新する処理がここ
    return {"message": "商品を更新", "item_id": item_id, "item": item}

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    # 実際にはDBから削除する処理がここ
    return {"message": "商品を削除", "item_id": item_id}