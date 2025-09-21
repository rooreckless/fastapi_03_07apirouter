from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

def _load_environment_variables():
    """環境変数ファイルを読み込む"""
    current_dir = Path(__file__).parent.parent.parent
    test_env_path = current_dir.parent / ".envs" / "test" / ".env"
    local_env_path = current_dir.parent / ".envs" / "local" / "env_local"

    # 実行環境を判定して適切な環境変数ファイルを選択
    if os.getenv("PYTEST_CURRENT_TEST") or "pytest" in os.environ.get("_", "") or any("pytest" in arg for arg in os.environ.get("PYTHONPATH", "").split(":")):
        # pytest実行時: VSCodeローカル環境ではtest/.envを使用
        if test_env_path.exists():
            load_dotenv(test_env_path)
    elif os.path.exists("/.dockerenv") or os.getenv("PYTHONPATH") == "/fastapi":
        # Docker環境: local/env_localを使用（Docker Composeでのテスト実行時）
        if local_env_path.exists():
            load_dotenv(local_env_path)
    else:
        # その他の場合: test/.envを優先、なければlocal/env_localを使用
        if test_env_path.exists():
            load_dotenv(test_env_path)
        elif local_env_path.exists():
            load_dotenv(local_env_path)

# 環境変数を読み込む
_load_environment_variables()

DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URLがNoneの場合のデフォルト値を設定
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# さまざまなユースケースから使われるDBのセッション開始と自動終了部分の共通化パーツとなる関数
async def get_db():
    async with AsyncSessionLocal() as session:
        #↑ 非同期コンテキストマネージャーにより、セッションを開始し、終了時に自動的にクローズします（例外が出ても確実に __aexit__() が呼ばれる）
        yield session
        # ↑yield sessionはFastAPI の Depends() によって依存注入されるオブジェクトとして session を返します