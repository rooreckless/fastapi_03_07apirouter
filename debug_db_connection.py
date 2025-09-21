#!/usr/bin/env python3
"""
AWS環境でのデータベース接続をデバッグするスクリプト
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_db_connection():
    """データベース接続をテストする"""
    
    # 環境変数を表示（パスワードは一部マスク）
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # パスワード部分をマスク
        masked_url = database_url.replace(
            database_url.split('://')[1].split('@')[0].split(':')[1],
            '***'
        )
        print(f"DATABASE_URL: {masked_url}")
    else:
        print("DATABASE_URL is not set!")
        return
    
    try:
        print("Creating database engine...")
        engine = create_async_engine(database_url, echo=True)
        
        print("Testing database connection...")
        async with engine.begin() as conn:
            # 基本的な接続テスト
            result = await conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            print(f"✅ Basic connection test passed: {test_value}")
            
            # テーブル存在確認
            tables = ["users", "categories", "items", "item_category"]
            for table in tables:
                try:
                    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"✅ Table '{table}' exists with {count} rows")
                except Exception as e:
                    print(f"❌ Table '{table}' error: {e}")
            
            # データベース情報の確認
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"📊 PostgreSQL version: {version}")
            
            result = await conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            print(f"📊 Current database: {db_name}")
            
        print("✅ All database tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'engine' in locals():
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db_connection())