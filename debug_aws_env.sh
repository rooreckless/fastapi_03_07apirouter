#!/bin/bash

# AWS環境デバッグ用スクリプト
echo "=== AWS環境デバッグ開始 ==="

echo "1. 環境変数の確認"
echo "DATABASE_URL: $DATABASE_URL"
echo "JWT_SECRET_KEY: ${JWT_SECRET_KEY:0:10}..." # 最初の10文字のみ表示
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"

echo ""
echo "2. データベース接続テスト"
python3 -c "
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test():
    try:
        engine = create_async_engine(os.getenv('DATABASE_URL'))
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT 1'))
            print(f'✅ DB接続成功: {result.scalar()}')
        await engine.dispose()
    except Exception as e:
        print(f'❌ DB接続失敗: {e}')

asyncio.run(test())
"

echo ""
echo "3. テーブル存在確認"
python3 -c "
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_tables():
    try:
        engine = create_async_engine(os.getenv('DATABASE_URL'))
        async with engine.begin() as conn:
            for table in ['users', 'categories', 'items', 'item_category']:
                try:
                    result = await conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
                    count = result.scalar()
                    print(f'✅ テーブル {table}: {count}行')
                except Exception as e:
                    print(f'❌ テーブル {table}: {e}')
        await engine.dispose()
    except Exception as e:
        print(f'❌ テーブル確認失敗: {e}')

asyncio.run(check_tables())
"

echo ""
echo "4. FastAPIアプリケーションの起動確認"
python3 -c "
try:
    from app.main import app
    print('✅ FastAPIアプリケーション正常にインポートされました')
except Exception as e:
    print(f'❌ FastAPIアプリケーションインポート失敗: {e}')
"

echo "=== AWS環境デバッグ終了 ==="