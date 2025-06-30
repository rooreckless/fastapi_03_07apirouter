# ⑤プレゼンテーション層
# app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.category_dto import CategoryCreateDTO, CategoryReadDTO
from app.db.database import get_db
from app.infrastructure.sqlalchemy.repositories.category_repo_impl import SQLAlchemyCategoryRepository
from app.usecases.category.create_category import CreateCategoryUseCase
from app.usecases.category.list_categories import ListCategoriesUseCase
from app.usecases.category.get_category import GetCategoryUseCase

router = APIRouter(prefix="/categories")

# DIチェーン
def get_category_repo(db: AsyncSession = Depends(get_db)):
    return SQLAlchemyCategoryRepository(db)

def get_create_uc(repo=Depends(get_category_repo)):
    return CreateCategoryUseCase(repo)

def get_list_uc(repo=Depends(get_category_repo)):
    return ListCategoriesUseCase(repo)
def get_get_uc(repo=Depends(get_category_repo)):
    return GetCategoryUseCase(repo)

@router.post("/", response_model=CategoryReadDTO)
async def create(dto: CategoryCreateDTO,
                 uc: CreateCategoryUseCase = Depends(get_create_uc)):
    category = await uc.execute(dto.category_name)
    return CategoryReadDTO(category_id=category.id, category_name=category.name)

@router.get("/", response_model=list[CategoryReadDTO])
async def list_all(uc: ListCategoriesUseCase = Depends(get_list_uc)):
    categories = await uc.execute()
    return [CategoryReadDTO(category_id=c.id, category_name=c.name) for c in categories]

@router.get("/{category_id}", response_model=CategoryReadDTO)
async def get_item(category_id: int,
                   uc: GetCategoryUseCase = Depends(get_get_uc)):
    category = await uc.execute(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryReadDTO(category_id=category.id, category_name=category.name)
