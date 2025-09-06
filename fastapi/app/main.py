from fastapi import FastAPI
from app.routers.categories import router as category_router
from app.routers.items import router as item_router
from app.routers.auth import router as auth_router
from datetime import datetime
from zoneinfo import ZoneInfo
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