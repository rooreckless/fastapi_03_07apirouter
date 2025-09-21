from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# 上位階層の環境変数ファイルを読み込み
# テスト環境の場合はtest/.env、通常はlocal/env_localを使用
current_dir = Path(__file__).parent.parent.parent
test_env_path = current_dir.parent / ".envs" / "test" / ".env"
local_env_path = current_dir.parent / ".envs" / "local" / "env_local"

# テスト実行時か通常実行かを判定してファイルを選択
if os.getenv("PYTEST_CURRENT_TEST") or "pytest" in os.environ.get("_", ""):
    # pytestで実行されている場合はtest/.envを使用
    if test_env_path.exists():
        load_dotenv(test_env_path)
else:
    # 通常実行時はlocal/env_localを使用
    if local_env_path.exists():
        load_dotenv(local_env_path)

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