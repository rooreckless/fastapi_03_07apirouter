# ⑤プレゼンテーション層
# app/routers/items.py
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.item_dto import ItemCreateDTO, ItemReadDTO, ItemUpdateDTO, ItemUpdateNameDTO
from app.dto.user_dto import UserReadDTO
from app.db.database import get_db
from app.infrastructure.sqlalchemy.repo_imples.item_repo_impl import SQLAlchemyItemRepository
from app.usecases.item.create_item import CreateItemUseCase
from app.usecases.item.list_items import ListItemsUseCase
from app.usecases.item.get_item import GetItemUseCase
from app.usecases.item.update_item import UpdateItemUseCase
from app.usecases.item.update_item_name import UpdateItemNameUseCase
from app.usecases.item.delete_item import DeleteItemUseCase
from app.routers.auth import get_current_user

router = APIRouter(prefix="/items", tags=["item"])

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
async def create(
    dto: ItemCreateDTO,
    uc: CreateItemUseCase = Depends(get_create_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """アイテムを作成（認証必須）"""
    category_ids = dto.category_ids or []
    item = await uc.execute(dto.item_name, category_ids, current_user.user_id)
    return ItemReadDTO(
        item_id=item.id, 
        item_name=item.name, 
        category_ids=item.category_ids,
        created_by=item.created_by,
        updated_by=item.updated_by,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.get("/", response_model=list[ItemReadDTO])
async def list_all(uc: ListItemsUseCase = Depends(get_list_uc)):
    items = await uc.execute()
    return [
        ItemReadDTO(
            item_id=item.id, 
            item_name=item.name, 
            category_ids=item.category_ids,
            created_by=item.created_by,
            updated_by=item.updated_by,
            created_at=item.created_at,
            updated_at=item.updated_at
        )
        for item in items
    ]

@router.get("/{item_id}", response_model=ItemReadDTO)
async def get_item(item_id: int,
                   uc: GetItemUseCase = Depends(get_get_uc)):
    item = await uc.execute(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_ids=item.category_ids,
        created_by=item.created_by,
        updated_by=item.updated_by,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.put("/{item_id}", response_model=ItemReadDTO)
async def update_item(
    item_id: int,
    dto: ItemUpdateDTO,
    uc: UpdateItemUseCase = Depends(get_update_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """アイテムを更新（認証必須）"""
    item = await uc.execute(item_id, dto.item_name, dto.category_ids, current_user.user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_ids=item.category_ids,
        created_by=item.created_by,
        updated_by=item.updated_by,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.put("/{item_id}/name_body", response_model=ItemReadDTO)
async def update_name_body(
    item_id: int,
    new_name: str = Body(..., embed=True),
    uc: UpdateItemNameUseCase = Depends(get_update_name_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """アイテム名を更新（Body版・認証必須）"""
    try:
        item = await uc.execute(item_id, new_name, current_user.user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_ids=item.category_ids,
        created_by=item.created_by,
        updated_by=item.updated_by,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.put("/{item_id}/name_dto", response_model=ItemReadDTO)
async def update_name_dto(
    item_id: int,
    dto: ItemUpdateNameDTO,
    uc: UpdateItemNameUseCase = Depends(get_update_name_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """アイテム名を更新（DTO版・認証必須）"""
    try:
        item = await uc.execute(item_id, dto.item_name, current_user.user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemReadDTO(
        item_id=item.id,
        item_name=item.name,
        category_ids=item.category_ids,
        created_by=item.created_by,
        updated_by=item.updated_by,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int, 
    uc: DeleteItemUseCase = Depends(get_delete_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """アイテムを削除（認証必須）"""
    try:
        await uc.execute(item_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")
    # なにも返さなくていい。(他のユースケースだと、レコードをDTOで返すが、削除だと不要)
    return None