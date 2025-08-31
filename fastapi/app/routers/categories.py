# ⑤プレゼンテーション層
# app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.category_dto import CategoryCreateDTO, CategoryReadDTO, CategoryUpdateDTO
from app.dto.user_dto import UserReadDTO
from app.db.database import get_db
from app.infrastructure.sqlalchemy.repo_imples.category_repo_impl import SQLAlchemyCategoryRepository
from app.usecases.category.create_category import CreateCategoryUseCase
from app.usecases.category.list_categories import ListCategoriesUseCase
from app.usecases.category.get_category import GetCategoryUseCase
from app.usecases.category.update_category import UpdateCategoryUseCase
from app.routers.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["category"])

# DIチェーン
def get_category_repo(db: AsyncSession = Depends(get_db)):
    return SQLAlchemyCategoryRepository(db)

def get_create_uc(repo=Depends(get_category_repo)):
    return CreateCategoryUseCase(repo)

def get_list_uc(repo=Depends(get_category_repo)):
    return ListCategoriesUseCase(repo)
def get_get_uc(repo=Depends(get_category_repo)):
    return GetCategoryUseCase(repo)
def get_update_uc(repo=Depends(get_category_repo)):
    return UpdateCategoryUseCase(repo)

# エンドポイント


@router.post("/", response_model=CategoryReadDTO)
async def create(
    dto: CategoryCreateDTO,
    uc: CreateCategoryUseCase = Depends(get_create_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """カテゴリを作成（認証必須）"""
    category = await uc.execute(dto.category_name, current_user.user_id)
    return CategoryReadDTO(
        category_id=category.id, 
        category_name=category.name,
        created_by=category.created_by,
        updated_by=category.updated_by,
        created_at=category.created_at,
        updated_at=category.updated_at
    )


@router.get("/", response_model=list[CategoryReadDTO])
async def list_all(uc: ListCategoriesUseCase = Depends(get_list_uc)):
    categories = await uc.execute()
    return [CategoryReadDTO(
        category_id=c.id, 
        category_name=c.name,
        created_by=c.created_by,
        updated_by=c.updated_by,
        created_at=c.created_at,
        updated_at=c.updated_at
    ) for c in categories]


@router.get("/{category_id}", response_model=CategoryReadDTO)
async def get_category(category_id: int, 
                       uc: GetCategoryUseCase = Depends(get_get_uc)):
    category = await uc.execute(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryReadDTO(
        category_id=category.id, 
        category_name=category.name,
        created_by=category.created_by,
        updated_by=category.updated_by,
        created_at=category.created_at,
        updated_at=category.updated_at
    )


@router.put("/{category_id}", response_model=CategoryReadDTO)
async def update_category(
    category_id: int,
    dto: CategoryUpdateDTO,
    uc: UpdateCategoryUseCase = Depends(get_update_uc),
    current_user: UserReadDTO = Depends(get_current_user)
):
    """カテゴリを更新（認証必須）"""
    category = await uc.execute(category_id, dto.category_name, current_user.user_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryReadDTO(
        category_id=category.id, 
        category_name=category.name,
        created_by=category.created_by,
        updated_by=category.updated_by,
        created_at=category.created_at,
        updated_at=category.updated_at
    )