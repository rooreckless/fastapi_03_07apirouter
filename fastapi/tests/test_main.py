"""main.py テストモジュール."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


class TestMainModule:
    """main.pyモジュールのテストクラス."""

    def test_app_instance_creation(self):
        """正常系: FastAPIアプリケーションインスタンスが作成される."""
        assert isinstance(app, FastAPI)
        assert hasattr(app, 'include_router')
        assert hasattr(app, 'get')
        assert hasattr(app, 'post')

    def test_app_routers_included(self):
        """正常系: ルーターが正しくアプリケーションに含まれている."""
        # アプリケーションのルートを確認
        routes = [getattr(route, 'path', '') for route in app.routes]
        
        # カテゴリとアイテムのルートが含まれていることを確認
        category_routes = [route for route in routes if '/categories' in route]
        item_routes = [route for route in routes if '/items' in route]
        
        assert len(category_routes) > 0, "Category routes should be included"
        assert len(item_routes) > 0, "Item routes should be included"

    def test_root_endpoint_exists(self):
        """正常系: ルートエンドポイントが存在する."""
        routes = [getattr(route, 'path', '') for route in app.routes]
        assert "/" in routes

    @pytest.mark.asyncio
    async def test_root_endpoint_response(self):
        """正常系: ルートエンドポイントが正しいレスポンスを返す."""
        from app.main import root
        
        response = await root()
        expected_response = {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}
        
        assert response == expected_response
        assert isinstance(response, dict)
        assert "message" in response

    def test_root_endpoint_via_test_client(self):
        """正常系: TestClientを使用したルートエンドポイントのテスト."""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}

    def test_app_openapi_generation(self):
        """正常系: OpenAPIスキーマが生成される."""
        openapi_schema = app.openapi()
        
        assert openapi_schema is not None
        assert "openapi" in openapi_schema
        assert "info" in openapi_schema
        assert "paths" in openapi_schema

    def test_app_routes_count(self):
        """正常系: 期待される数のルートが登録されている."""
        # 最低限ルートエンドポイント（"/"）は存在するはず
        routes = [route for route in app.routes]
        assert len(routes) >= 1

    def test_app_middleware_stack(self):
        """正常系: ミドルウェアスタックが正しく構成されている."""
        # FastAPIのデフォルトミドルウェアが存在することを確認
        assert hasattr(app, 'middleware_stack')
        assert app.middleware_stack is not None

    def test_app_debug_mode(self):
        """正常系: アプリケーションのデバッグ設定を確認."""
        # FastAPIアプリケーションの基本属性を確認
        assert hasattr(app, 'debug')
        # debugがbool型であることを確認
        assert isinstance(app.debug, bool)

    def test_app_title_and_version(self):
        """正常系: アプリケーションのタイトルとバージョンを確認."""
        # デフォルトのタイトルとバージョンを確認
        assert hasattr(app, 'title')
        assert hasattr(app, 'version')
        assert isinstance(app.title, str)
        assert isinstance(app.version, str)

    def test_router_imports(self):
        """正常系: ルーターのインポートが正しく行われている."""
        # app.main モジュールの内容を確認
        import app.main
        
        assert hasattr(app.main, 'category_router')
        assert hasattr(app.main, 'item_router')
        assert hasattr(app.main, 'app')

    def test_category_router_inclusion(self):
        """正常系: カテゴリルーターが正しく含まれている."""
        # カテゴリ関連のエンドポイントが存在することを確認
        paths = [getattr(route, 'path', '') for route in app.routes]
        category_paths = [path for path in paths if 'categories' in path]
        
        # 少なくとも1つのカテゴリ関連パスが存在すること
        assert len(category_paths) > 0

    def test_item_router_inclusion(self):
        """正常系: アイテムルーターが正しく含まれている."""
        # アイテム関連のエンドポイントが存在することを確認
        paths = [getattr(route, 'path', '') for route in app.routes]
        item_paths = [path for path in paths if 'items' in path]
        
        # 少なくとも1つのアイテム関連パスが存在すること
        assert len(item_paths) > 0

    def test_app_state_initialization(self):
        """正常系: アプリケーション状態が正しく初期化されている."""
        # FastAPIアプリケーションの状態オブジェクトを確認
        assert hasattr(app, 'state')
        assert app.state is not None

    def test_root_endpoint_method(self):
        """正常系: ルートエンドポイントのHTTPメソッドが正しい."""
        root_routes = [route for route in app.routes if getattr(route, 'path', '') == "/"]
        assert len(root_routes) > 0
        
        # ルートエンドポイントがGETメソッドをサポートしていることを確認
        root_route = root_routes[0]
        methods = getattr(root_route, 'methods', set())
        assert "GET" in methods

    def test_app_exception_handlers(self):
        """正常系: 例外ハンドラーが適切に設定されている."""
        # FastAPIのデフォルト例外ハンドラーが存在することを確認
        assert hasattr(app, 'exception_handlers')
        assert isinstance(app.exception_handlers, dict)

    def test_app_dependency_overrides(self):
        """正常系: 依存性オーバーライドが設定可能である."""
        # dependency_overridesが存在し、辞書型であることを確認
        assert hasattr(app, 'dependency_overrides')
        assert isinstance(app.dependency_overrides, dict)

    def test_root_endpoint_content_type(self):
        """正常系: ルートエンドポイントが正しいContent-Typeを返す."""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_app_lifespan_events(self):
        """正常系: ライフサイクルイベントハンドラーが設定可能である."""
        # FastAPIのライフサイクルイベント属性を確認
        assert hasattr(app, 'router')
        assert hasattr(app.router, 'lifespan')

    def test_commented_code_does_not_affect_app(self):
        """エッジケース: コメントアウトされたコードがアプリケーションに影響しない."""
        # コメントアウトされたエンドポイントが実際には存在しないことを確認
        paths = [getattr(route, 'path', '') for route in app.routes]
        
        # コメントアウトされた '/with_depends' や '/no_depends' が存在しないことを確認
        assert "/with_depends" not in paths
        assert "/no_depends" not in paths

    def test_app_mount_points(self):
        """正常系: マウントポイントが適切に設定されている."""
        # FastAPIアプリケーションのマウント情報を確認
        assert hasattr(app, 'mount')
        # mountsが存在することを確認（空でも良い）
        assert hasattr(app, 'routes')

    @pytest.mark.asyncio
    async def test_root_endpoint_async_behavior(self):
        """正常系: ルートエンドポイントの非同期動作を確認."""
        from app.main import root
        
        # 非同期関数として正しく動作することを確認
        result = await root()
        
        assert result == {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}

    def test_fastapi_import_success(self):
        """正常系: FastAPIが正しくインポートされている."""
        # FastAPIクラスがインポートされていることを確認
        assert hasattr(FastAPI, '__name__')

    def test_routers_import_success(self):
        """正常系: ルーターが正しくインポートされている."""
        # ルーターがインポートされていることを確認
        from app.routers.categories import router as category_router
        from app.routers.items import router as item_router
        
        assert category_router is not None
        assert item_router is not None

    def test_app_routes_methods(self):
        """正常系: 各ルートが適切なHTTPメソッドをサポートしている."""
        # 各ルートがHTTPメソッドを持っていることを確認
        for route in app.routes:
            methods = getattr(route, 'methods', None)
            if methods is not None:
                assert isinstance(methods, (set, frozenset))
                assert len(methods) > 0

    def test_multiple_test_client_instances(self):
        """エッジケース: 複数のTestClientインスタンスが作成できる."""
        client1 = TestClient(app)
        client2 = TestClient(app)
        
        response1 = client1.get("/")
        response2 = client2.get("/")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json()

    def test_app_invalid_route_access(self):
        """異常系: 存在しないルートへのアクセス."""
        client = TestClient(app)
        response = client.get("/nonexistent")
        
        assert response.status_code == 404

    def test_app_with_mocked_routers(self):
        """エッジケース: ルーターをモック化した場合の動作."""
        with patch('app.main.category_router') as mock_category_router, \
             patch('app.main.item_router') as mock_item_router:
            
            mock_category_router.routes = []
            mock_item_router.routes = []
            
            # モックされたルーターでもアプリケーションが動作することを確認
            client = TestClient(app)
            response = client.get("/")
            
            assert response.status_code == 200
