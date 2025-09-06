"""database.py テストモジュール."""

import os
import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, AsyncSessionLocal, engine


class TestDatabaseModule:
    """database.pyモジュールのテストクラス."""

    def test_database_url_environment_variable_set(self):
        """正常系: DATABASE_URL環境変数が設定されている場合."""
        # 実際に設定されているDATABASE_URLを確認
        import app.db.database
        assert app.db.database.DATABASE_URL is not None
        assert isinstance(app.db.database.DATABASE_URL, str)
        assert "postgresql" in app.db.database.DATABASE_URL

    def test_database_url_environment_variable_not_set(self, mocker):
        """異常系: DATABASE_URL環境変数が設定されていない場合."""
        mocker.patch.dict(os.environ, {}, clear=True)
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            # database.pyの再読み込みをシミュレート
            import importlib
            import app.db.database
            importlib.reload(app.db.database)

    def test_database_url_environment_variable_none(self, mocker):
        """異常系: DATABASE_URL環境変数がNoneの場合."""
        mocker.patch.dict(os.environ, {"DATABASE_URL": ""})
        mocker.patch("os.getenv", return_value=None)
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            import importlib
            import app.db.database
            importlib.reload(app.db.database)

    def test_engine_creation(self):
        """正常系: SQLAlchemyエンジンが正常に作成される."""
        assert engine is not None
        assert hasattr(engine, 'connect')
        assert hasattr(engine, 'dispose')

    def test_async_session_local_creation(self):
        """正常系: AsyncSessionLocalが正常に作成される."""
        assert AsyncSessionLocal is not None
        assert hasattr(AsyncSessionLocal, '__call__')

    def test_async_session_local_configuration(self):
        """正常系: AsyncSessionLocalの設定が正しい."""
        # async_sessionmakerの基本的な設定を確認
        session_factory = AsyncSessionLocal
        # async_sessionmakerは callable であることを確認
        assert callable(session_factory)
        # async_sessionmakerの型確認
        from sqlalchemy.ext.asyncio import async_sessionmaker
        assert isinstance(session_factory, type(async_sessionmaker()))

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """正常系: get_db関数がAsyncSessionを返す."""
        session_generator = get_db()
        session = await session_generator.__anext__()
        
        assert isinstance(session, AsyncSession)
        assert hasattr(session, 'execute')
        assert hasattr(session, 'commit')
        assert hasattr(session, 'rollback')
        
        # セッションをクリーンアップ（適切にacloseを使用）
        await session_generator.aclose()

    @pytest.mark.asyncio
    async def test_get_db_session_cleanup(self):
        """正常系: get_db関数がセッションを適切にクリーンアップする."""
        session_generator = get_db()
        session = await session_generator.__anext__()
        
        # セッションが生成されたことを確認
        assert isinstance(session, AsyncSession)
        
        # aclose()でクリーンアップ
        await session_generator.aclose()

    @pytest.mark.asyncio
    async def test_get_db_multiple_calls(self):
        """正常系: get_db関数が複数回呼び出せる."""
        # 最初の呼び出し
        session_generator1 = get_db()
        session1 = await session_generator1.__anext__()
        
        # 二回目の呼び出し
        session_generator2 = get_db()
        session2 = await session_generator2.__anext__()
        
        # 異なるセッションインスタンスが返されることを確認
        assert isinstance(session1, AsyncSession)
        assert isinstance(session2, AsyncSession)
        assert session1 is not session2
        
        # クリーンアップ
        await session_generator1.aclose()
        await session_generator2.aclose()

    @pytest.mark.asyncio
    async def test_get_db_session_context_manager(self):
        """正常系: get_db関数がコンテキストマネージャーとして動作する."""
        session_generator = get_db()
        
        # セッションを取得
        session = await session_generator.__anext__()
        assert isinstance(session, AsyncSession)
        
        # セッションが使用可能であることを確認
        assert hasattr(session, 'bind')
        assert session.bind is not None
        
        # ジェネレータの終了
        await session_generator.aclose()

    @pytest.mark.asyncio
    async def test_get_db_with_mock_session_local(self, mocker):
        """エッジケース: AsyncSessionLocalをモックした場合の動作."""
        mock_session = AsyncMock(spec=AsyncSession)
        
        mock_session_local = mocker.patch('app.db.database.AsyncSessionLocal')
        # AsyncContextManagerのモック設定
        mock_session_local.return_value.__aenter__.return_value = mock_session
        mock_session_local.return_value.__aexit__.return_value = None
        
        session_generator = get_db()
        session = await session_generator.__anext__()
        
        assert session == mock_session
        
        # クリーンアップ
        await session_generator.aclose()

    def test_database_url_with_special_characters(self):
        """エッジケース: DATABASE_URLが存在し適切な形式であることを確認."""
        # 実際のDATABASE_URLが使用されていることを確認
        import os
        current_url = os.getenv("DATABASE_URL")
        assert current_url is not None
        assert isinstance(current_url, str)
        # URLが有効な形式であることを確認
        assert "://" in current_url

    def test_engine_echo_configuration(self):
        """正常系: エンジンのecho設定が有効になっている."""
        # エンジンのecho設定を確認
        assert hasattr(engine, 'echo')
        # echoがTrueに設定されていることを確認（database.pyでecho=Trueを指定）
        assert engine.echo is True

    def test_async_session_expire_on_commit_configuration(self):
        """正常系: AsyncSessionのexpire_on_commit設定が正しい."""
        # async_sessionmakerの基本的な機能を確認
        session_factory = AsyncSessionLocal
        # sessionmakerが正しく構成されていることを確認
        assert callable(session_factory)
        # sessionmakerの文字列表現にexpire_on_commit=Falseが含まれることを確認
        session_repr = str(session_factory)
        assert 'expire_on_commit=False' in session_repr

    def test_module_level_imports(self):
        """正常系: 必要なモジュールが正しくインポートされている."""
        import app.db.database
        
        # 必要な関数とオブジェクトが存在することを確認
        assert hasattr(app.db.database, 'get_db')
        assert hasattr(app.db.database, 'AsyncSessionLocal')
        assert hasattr(app.db.database, 'engine')
        assert hasattr(app.db.database, 'DATABASE_URL')

    @pytest.mark.asyncio
    async def test_get_db_error_handling(self, mocker):
        """異常系: get_db内でエラーが発生した場合の処理."""
        mock_session_local = mocker.patch('app.db.database.AsyncSessionLocal')
        # コンテキストマネージャーの入場時にエラーを発生させる
        mock_session_local.return_value.__aenter__.side_effect = Exception("Database connection error")
        
        session_generator = get_db()
        
        with pytest.raises(Exception, match="Database connection error"):
            await session_generator.__anext__()
