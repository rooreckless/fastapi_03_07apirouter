from fastapi import APIRouter
from app.schemas.item import Item

router =APIRouter()

@router.get("/items/", response_model=dict)
async def read_items():
    # 実際にはDBから取得処理がここ
    return {"message": "商品一覧を表示", "items":[]}

@router.post("/items/", response_model=dict)
async def create_item(item: Item):
    # 実際にはDBに保存する処理がここ
    return {"message": "商品を作成", "item": item}

@router.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, item: Item):
    # 実際にはDBに更新する処理がここ
    return {"message": "商品を更新", "item_id": item_id, "item": item}

@router.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    # 実際にはDBから削除する処理がここ
    return {"message": "商品を削除", "item_id": item_id}