"""integrate_testsディレクトリ用の共通conftest.py

実際のPostgreSQLデータベースにアクセスする統合テスト用の設定
fastapi_dbを使用し、テストごとにトランザクションレベルで分離
"""
import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 全てのモデルをインポート
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.item_category_association import item_category


@pytest.fixture(scope="function")
def event_loop():
    """ファンクションスコープでasyncioイベントループを共有"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function") 
async def async_session():
    """
    テスト用のAsyncSessionを提供
    各テストでデータベースの状態を分離するため、テーブルクリアを使用
    """
    # fastapi_dbデータベースに直接接続
    engine = create_async_engine(
        "postgresql+asyncpg://fastapi_user:fastapi_pass@postgres:5432/fastapi_db",
        echo=False, 
        future=True
    )
    
    async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session_maker() as session:
        # テスト開始前に関連テーブルをクリア
        await session.execute(item_category.delete())
        await session.execute(CategoryORM.__table__.delete())
        await session.execute(ItemORM.__table__.delete())
        await session.commit()
        
        try:
            yield session
        finally:
            # テスト後にテーブルをクリア（データクリーンアップ）
            await session.execute(item_category.delete())
            await session.execute(CategoryORM.__table__.delete())
            await session.execute(ItemORM.__table__.delete())
            await session.commit()
    
    await engine.dispose()
