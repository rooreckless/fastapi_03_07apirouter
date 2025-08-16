from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

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