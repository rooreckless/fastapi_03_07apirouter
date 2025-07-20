# ⑤プレゼンテーション層
# app/routers/items.py
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.item_dto import ItemCreateDTO, ItemReadDTO, ItemUpdateDTO, ItemUpdateNameDTO
from app.db.database import get_db
from app.infrastructure.sqlalchemy.repositories.item_repo_impl import SQLAlchemyItemRepository
from app.usecases.item.create_item import CreateItemUseCase
from app.usecases.item.list_items import ListItemsUseCase
from app.usecases.item.get_item import GetItemUseCase
from app.usecases.item.update_item import UpdateItemUseCase
from app.usecases.item.update_item_name import UpdateItemNameUseCase
from app.usecases.item.delete_item import DeleteItemUseCase

router = APIRouter(prefix="/items")

# DIチェーン
def get_item_repo(db: AsyncSession = Depends(get_db)):
    return SQLAlchemyItemRepository(db)

def get_create_uc(repo=Depends(get_item_repo)):
    return CreateItemUseCase(repo)

def get_list_uc(repo=Depends(get_item_repo)):
    return ListItemsUseCase(repo)

def get_get_uc(repo=Depends(get_item_repo)):
    return GetItemUseCase(repo)

def get_update_uc(repo=Depends(get_item_repo)):
    return UpdateItemUseCase(repo)

def get_update_name_uc(repo=Depends(get_item_repo)):
    return UpdateItemNameUseCase(repo)

def get_delete_uc(repo=Depends(get_item_repo)):
    return DeleteItemUseCase(repo)

# エンドポイント
# 各メソッドの引数dtoはスキーマの型、ucでユースケースの型を指定。ただし、ucについてはDependsでユースケースをラップし、fastapiまかせにする
@router.post("/", response_model=ItemReadDTO)
async def create(dto: ItemCreateDTO,
                 uc: CreateItemUseCase = Depends(get_create_uc)):
    item = await uc.execute(dto.item_name, dto.category_id)
    return ItemReadDTO(item_id=item.id, item_name=item.name, category_id=item.category_id)

@router.get("/", response_model=list[ItemReadDTO])
async def list_all(uc: ListItemsUseCase = Depends(get_list_uc)):
    items = await uc.execute()
    return [ItemReadDTO(item_id=c.id, item_name=c.name, category_id=c.category_id) for c in items]

@router.get("/{item_id}", response_model=ItemReadDTO)
async def get_item(item_id: int,
                   uc: GetItemUseCase = Depends(get_get_uc)):
    item = await uc.execute(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemReadDTO(item_id=item.id, item_name=item.name, category_id=item.category_id)

@router.put("/{item_id}", response_model=ItemReadDTO)
async def update_item(item_id: int,
                      dto: ItemUpdateDTO,
                      uc: UpdateItemUseCase = Depends(get_update_uc)):
    item = await uc.execute(item_id, dto.item_name, dto.category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemReadDTO(item_id=item.id, item_name=item.name, category_id=item.category_id)

# Itemの一部更新(商品名のみ更新のルート)
# ただし、Itemの新しい名前はfastapi.Bodyを使い、リクエストボディの内容を直接取得する方法にしてる
@router.put("/{item_id}/name_body", response_model=ItemReadDTO)
async def update_name_body(
    item_id: int,
    new_name: str = Body(..., embed=True),
    uc: UpdateItemNameUseCase = Depends(get_update_name_uc)
):
    try:
        item = await uc.execute(item_id, new_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_id=item.category_id
    )

# Itemの一部更新(商品名のみ更新のルート)
# ただし、Itemの新しい名前はPydanticを使い、リクエストボディの内容はdtoがうける方法にしてる
# dtoケースは複数の入力値、複数のフィールドがある場合に使うべきだが、比較のため実施している
@router.put("/{item_id}/name_dto", response_model=ItemReadDTO)
async def update_name_dto(
    item_id: int,
    dto: ItemUpdateNameDTO,
    uc: UpdateItemNameUseCase = Depends(get_update_name_uc)
):
    try:
        item = await uc.execute(item_id, dto.item_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_id=item.category_id
    )

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, uc: DeleteItemUseCase = Depends(get_delete_uc)):
    try:
        await uc.execute(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="str(e)")
    # なにも返さなくていい。(他のユースケースだと、レコードをDTOで返すが、削除だと不要)
    return None