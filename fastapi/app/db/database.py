from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# さまざまなユースケースから使われるDBのセッション開始と自動終了部分の共通化パーツとなる関数
async def get_db():
    async with AsyncSessionLocal() as session:
        #↑ 非同期コンテキストマネージャーにより、セッションを開始し、終了時に自動的にクローズします（例外が出ても確実に __aexit__() が呼ばれる）
        yield session
        # ↑yield sessionはFastAPI の Depends() によって依存注入されるオブジェクトとして session を返します