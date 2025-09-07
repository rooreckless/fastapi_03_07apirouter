from fastapi import FastAPI, HTTPException, Depends
from app.routers.categories import router as category_router
from app.routers.items import router as item_router
from app.routers.auth import router as auth_router
from app.db.database import get_db
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Swagger UIでの認証設定
app = FastAPI(
    title="FastAPI Authentication Demo",
    description="""
    認証機能付きFastAPI アプリケーション
    
    ## 認証方法
    1. /auth/token エンドポイントでトークンを取得
    2. 右上の 🔒 Authorize ボタンをクリック
    3. username: メールアドレス, password: パスワードを入力
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ルーターをappに追加
app.include_router(auth_router)     # 認証関連
app.include_router(category_router) # カテゴリ関連
app.include_router(item_router)     # アイテム関連

# ↓app.routerとは関係のないルート
@app.get("/")
async def root():
    return {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}

# fastapi/app/main.py または適切なルーターファイルに追加
@app.get("/health")
async def health_check():
    """
    ヘルスチェック用エンドポイント
    ECSやロードバランサーからの監視に使用
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(),
        "service": "fastapi-app"
    }

# データベース初期化エンドポイント
@app.post("/admin/init-database")
async def init_database_tables(db: AsyncSession = Depends(get_db)):
    """
    データベーステーブルを初期化するエンドポイント
    セキュリティのため、本番環境では削除または認証を追加してください
    """
    try:
        # DDLスクリプトを実行
        ddl_script = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            user_id int4 NOT NULL,
            mail_address varchar NOT NULL,
            hashed_password varchar NOT NULL,
            full_name varchar NULL,
            is_active bool DEFAULT true NOT NULL,
            is_superuser bool DEFAULT false NOT NULL,
            created_at timestamptz DEFAULT now() NOT NULL,
            updated_at timestamptz DEFAULT now() NOT NULL,
            CONSTRAINT users_mail_address_unique UNIQUE (mail_address),
            CONSTRAINT users_pk PRIMARY KEY (user_id)
        );

        -- Categories table
        CREATE TABLE IF NOT EXISTS categories (
            category_id int4 NOT NULL,
            category_name varchar NOT NULL,
            created_by int4 NULL,
            updated_by int4 NULL,
            created_at timestamptz DEFAULT now() NOT NULL,
            updated_at timestamptz DEFAULT now() NOT NULL,
            CONSTRAINT categories_pk PRIMARY KEY (category_id),
            CONSTRAINT categoryies_unique UNIQUE (category_name),
            CONSTRAINT fk_users_pk1 FOREIGN KEY (created_by) REFERENCES users(user_id),
            CONSTRAINT fk_users_pk2 FOREIGN KEY (updated_by) REFERENCES users(user_id)
        );

        -- Items table
        CREATE TABLE IF NOT EXISTS items (
            item_id int4 NOT NULL,
            item_name varchar NOT NULL,
            created_by int4 NULL,
            updated_by int4 NULL,
            created_at timestamptz DEFAULT now() NOT NULL,
            updated_at timestamptz DEFAULT now() NOT NULL,
            CONSTRAINT item_pk PRIMARY KEY (item_id),
            CONSTRAINT fk_users_pk1 FOREIGN KEY (updated_by) REFERENCES users(user_id),
            CONSTRAINT fk_users_pk2 FOREIGN KEY (created_by) REFERENCES users(user_id)
        );

        -- Item_category table
        CREATE TABLE IF NOT EXISTS item_category (
            item_id int4 NOT NULL,
            category_id int4 NOT NULL,
            CONSTRAINT item_category_pk PRIMARY KEY (item_id, category_id),
            CONSTRAINT item_category_categories_fk FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
            CONSTRAINT item_category_items_fk FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
        );
        """
        
        # SQLを分割して実行
        statements = [stmt.strip() for stmt in ddl_script.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                await db.execute(text(statement))
        
        await db.commit()
        
        return {
            "status": "success",
            "message": "データベーステーブルが正常に初期化されました",
            "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(),
            "tables_created": ["users", "categories", "items", "item_category"]
        }
    
    except Exception as e:
        await db.rollback()
        logger.error(f"データベース初期化エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"データベース初期化に失敗しました: {str(e)}")

# データベースのテーブル確認エンドポイント
@app.get("/admin/check-database")
async def check_database_tables(db: AsyncSession = Depends(get_db)):
    """
    データベーステーブルの存在確認
    """
    try:
        # テーブル一覧を取得
        result = await db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "status": "success",
            "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(),
            "tables": tables,
            "table_count": len(tables)
        }
    
    except Exception as e:
        logger.error(f"データベース確認エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"データベース確認に失敗しました: {str(e)}")

# より詳細なヘルスチェック（データベース接続確認付き）
@app.get("/health/detailed")
async def detailed_health_check():
    """
    詳細なヘルスチェック（データベース接続確認など）
    """
    try:
        # データベース接続確認
        # 実際のデータベース接続コードに応じて調整
        return {
            "status": "healthy",
            "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(),
            "service": "fastapi-app",
            "database": "connected",
            "dependencies": "ok"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(),
            "service": "fastapi-app",
            "error": str(e)
        }
# import uuid
# def get_token():
#     token = str(uuid.uuid4())
#     print(f"Token generated: {token}")
#     return token

# @app.get("/with_depends")
# def read_with_depends(token: str = Depends(get_token)):
#     return {"token": token}

# @app.get("/no_depends")
# def read_no_depends(token: str = get_token()):  # 起動時に一度だけ実行される
#     return {"token": token}

#--- スキーマ---



#---ルート----
#------カテゴリ------

# @app.get("/categories/", response_model=dict)
# async def read_categories():
#     # 実際にはDBから取得処理がここ
#     return {"message": "カテゴリ一覧を表示", "categories":[]}

# @app.post("/categories/", response_model=dict)
# async def create_category(category: Category):
#     # 実際にはDBに保存する処理がここ
#     return {"message": "カテゴリを作成", "category": category}

# @app.put("/categories/{category_id}", response_model=dict)
# async def update_category(category_id: int, category: Category):
#     # 実際にはDBに更新する処理がここ
#     return {"message": "カテゴリを更新", "category_id": category_id, "category": category}

# @app.delete("/categories/{category_id}", response_model=dict)
# async def delete_category(category_id: int):
#     # 実際にはDBから削除する処理がここ
#     return {"message": "カテゴリを削除", "category_id": category_id}

#------商品------

# @app.get("/items/", response_model=dict)
# async def read_items():
#     # 実際にはDBから取得処理がここ
#     return {"message": "商品一覧を表示", "items":[]}

# @app.post("/items/", response_model=dict)
# async def create_item(item: Item):
#     # 実際にはDBに保存する処理がここ
#     return {"message": "商品を作成", "item": item}

# @app.put("/items/{item_id}", response_model=dict)
# async def update_item(item_id: int, item: Item):
#     # 実際にはDBに更新する処理がここ
#     return {"message": "商品を更新", "item_id": item_id, "item": item}

# @app.delete("/items/{item_id}", response_model=dict)
# async def delete_item(item_id: int):
#     # 実際にはDBから削除する処理がここ
#     return {"message": "商品を削除", "item_id": item_id}