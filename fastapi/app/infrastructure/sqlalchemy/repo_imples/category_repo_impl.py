# Infrastructure層 - Repository実装
# SQLAlchemyを使用したCategoryリポジトリの具象実装
# 責務：
# - 抽象リポジトリインターフェースの実装
# - データベースへのCRUD操作
# - Mapperを使用したドメインエンティティとORMモデル間の変換
# - トランザクション管理

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.mappers.category_mapper import CategoryMapper
from app.domain.category import Category
from app.abstract_repository.category_repository import CategoryRepository # 抽象リポジトリ

class SQLAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemyを使用したCategoryリポジトリの具象実装クラス"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.mapper = CategoryMapper()

    async def save(self, category: Category) -> None:
        """カテゴリを保存する（新規作成または更新）
        
        Args:
            category: 保存するCategoryエンティティ
        """
        # IDが0の場合は新しいIDを生成
        if category.id == 0:
            category.id = await self.next_identifier()
        
        # Mapperを使用してドメインエンティティをORMモデルに変換
        orm = self.mapper.to_orm(category)
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        category.id = orm.category_id   # エンティティへIDを返す

    async def list_all(self) -> list[Category]:
        """全カテゴリをリスト形式で取得
        
        Returns:
            list[Category]: カテゴリエンティティのリスト
        """
        res = await self.db.execute(select(CategoryORM))
        return self.mapper.to_domain_list(res.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        """IDによるカテゴリの取得
        
        Args:
            category_id: 取得するカテゴリのID
            
        Returns:
            Category | None: カテゴリエンティティまたはNone
        """
        result = await self.db.execute(
            select(CategoryORM).filter(CategoryORM.category_id == category_id)
        )
        row = result.scalar_one_or_none()
        return self.mapper.to_domain(row) if row else None
    
    async def next_identifier(self) -> int:
        """カテゴリのIDを生成するためのメソッド
        
        Returns:
            int: 新しいカテゴリID
        """
        # 最新のID値(=categoryテーブルの最大のid値)を持つレコードを取得
        result = await self.db.execute(select(CategoryORM.category_id).order_by(CategoryORM.category_id.desc()).limit(1))
        # そのレコードのID値を取得
        row = result.scalar_one_or_none()
        # もしレコードが存在しない場合は1を返す
        # 存在する場合はそのID値に1を足して返す
        return (row + 1) if row is not None else 1

    async def update(self, category: Category) -> None:
        """カテゴリを更新する
        
        Args:
            category: 更新するCategoryエンティティ
        """
        db_item = await self.db.get(CategoryORM, category.id)
        if db_item:
            db_item.category_name = category.name
            await self.db.commit()