# ⑤プレゼンテーション層
# app/routers/items.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.item_dto import ItemCreateDTO, ItemReadDTO
from app.db.database import get_db
from app.infrastructure.sqlalchemy.repositories.item_repo_impl import SQLAlchemyItemRepository
from app.usecases.item.create_item import CreateItemUseCase
from app.usecases.item.list_items import ListItemsUseCase

router = APIRouter(prefix="/items")

# DIチェーン
def get_item_repo(db: AsyncSession = Depends(get_db)):
    return SQLAlchemyItemRepository(db)

def get_create_uc(repo=Depends(get_item_repo)):
    return CreateItemUseCase(repo)

def get_list_uc(repo=Depends(get_item_repo)):
    return ListItemsUseCase(repo)

@router.post("/", response_model=ItemReadDTO)
async def create(dto: ItemCreateDTO,
                 uc: CreateItemUseCase = Depends(get_create_uc)):
    print("--dto--",dto)
    item = await uc.execute(dto.item_name, dto.category_id)
    return ItemReadDTO(item_id=item.id, item_name=item.name, category_id=item.category_id)

@router.get("/", response_model=list[ItemReadDTO])
async def list_all(uc: ListItemsUseCase = Depends(get_list_uc)):
    items = await uc.execute()
    return [ItemReadDTO(item_id=c.id, item_name=c.name, category_id=c.category_id) for c in items]
