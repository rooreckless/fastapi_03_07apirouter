"""integrate_testsディレクトリ用の共通conftest.py

実際のPostgreSQLデータベースにアクセスする統合テスト用の設定
fastapi_dbを使用し、テストごとにトランザクションレベルで分離
"""

import asyncio
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 全てのモデルをインポート
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.infrastructure.sqlalchemy.models.item_category_association import item_category
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.user_orm import UserORM


@pytest.fixture(scope="function")
def event_loop():
    """ファンクションスコープでasyncioイベントループを共有"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_session():
    """
    テスト用のAsyncSessionを提供
    各テストでデータベースの状態を分離するため、テーブルクリアを使用
    リポジトリのcommit操作にも対応
    """
    # 上位階層の環境変数を読み込み（実行環境に応じて適切なファイルを選択）
    current_dir = Path(__file__).parent.parent
    test_env_path = current_dir.parent / ".envs" / "test" / ".env"
    local_env_path = current_dir.parent / ".envs" / "local" / "env_local"
    
    # 実行環境を判定して適切な環境変数ファイルを選択
    if os.path.exists("/.dockerenv") or os.getenv("PYTHONPATH") == "/fastapi":
        # Docker環境: local/env_localを使用
        if local_env_path.exists():
            load_dotenv(local_env_path)
    else:
        # VSCodeローカル環境: test/.envを使用
        if test_env_path.exists():
            load_dotenv(test_env_path)

    # 環境変数からDATABASE_URLを取得
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set for integration tests")

    engine = create_async_engine(database_url, echo=False, future=True)

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # テスト開始前のクリーンアップ
    async with async_session_maker() as cleanup_session:
        await cleanup_session.execute(item_category.delete())
        await cleanup_session.execute(CategoryORM.__table__.delete())
        await cleanup_session.execute(ItemORM.__table__.delete())
        await cleanup_session.execute(UserORM.__table__.delete())
        await cleanup_session.commit()

    # テスト用セッション提供
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            # セッション終了時にロールバック（もしトランザクションが残っていた場合）
            try:
                await session.rollback()
            except Exception:
                pass

    # テスト後のクリーンアップ
    async with async_session_maker() as cleanup_session:
        await cleanup_session.execute(item_category.delete())
        await cleanup_session.execute(CategoryORM.__table__.delete())
        await cleanup_session.execute(ItemORM.__table__.delete())
        await cleanup_session.execute(UserORM.__table__.delete())
        await cleanup_session.commit()

    await engine.dispose()
