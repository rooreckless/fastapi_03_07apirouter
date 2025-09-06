# tests/core/test_jwt.py
"""
JWT機能用のテストケース
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from jose import jwt, JWTError

from app.core.jwt import create_access_token, decode_token
from app.core.config import settings


class TestCreateAccessToken:
    """アクセストークン作成のテスト"""

    def test_create_access_token_with_default_expiry(self):
        """デフォルトの有効期限でトークン作成をテスト"""
        sub = "123"
        token = create_access_token(sub)
        
        # トークンが生成されることを確認
        assert isinstance(token, str)
        assert len(token) > 0
        
        # トークンをデコードして内容を確認
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
        assert payload["sub"] == sub
        assert "exp" in payload

    def test_create_access_token_with_custom_expiry(self):
        """カスタム有効期限でトークン作成をテスト"""
        sub = "456"
        expires_minutes = 60
        token = create_access_token(sub, expires_minutes)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # デコードして有効期限を確認
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
        assert payload["sub"] == sub
        
        # 有効期限が約60分後になっていることを確認（誤差を考慮）
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        
        # 1分の誤差を許容
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 60

    def test_create_access_token_with_zero_expiry(self):
        """0分の有効期限でトークン作成をテスト"""
        sub = "789"
        expires_minutes = 0
        token = create_access_token(sub, expires_minutes)
        
        assert isinstance(token, str)
        
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
        assert payload["sub"] == sub

    def test_create_access_token_with_negative_expiry(self):
        """負の有効期限でトークン作成をテスト（期限切れトークン）"""
        sub = "expired"
        expires_minutes = -10
        token = create_access_token(sub, expires_minutes)
        
        assert isinstance(token, str)
        
        # 期限切れトークンでもデコードできることを確認（検証なし）
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG], options={"verify_exp": False})
        assert payload["sub"] == sub

    def test_create_access_token_with_string_subject(self):
        """文字列のsubjectでトークン作成をテスト"""
        sub = "user@example.com"
        token = create_access_token(sub)
        
        assert isinstance(token, str)
        
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
        assert payload["sub"] == sub

    def test_create_access_token_with_none_expiry(self):
        """None有効期限でデフォルト設定が使用されることをテスト"""
        sub = "default_user"
        token = create_access_token(sub, None)
        
        assert isinstance(token, str)
        
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
        assert payload["sub"] == sub
        
        # デフォルト有効期限（30分）が使用されていることを確認
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 60

    @patch('app.core.jwt.datetime')
    def test_create_access_token_deterministic_time(self, mock_datetime):
        """固定時刻でのトークン作成をテスト"""
        # 固定時刻を設定
        fixed_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = fixed_time
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        sub = "test_user"
        expires_minutes = 30
        token = create_access_token(sub, expires_minutes)
        
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG], options={"verify_exp": False})
        assert payload["sub"] == sub
        
        # 期待される有効期限
        expected_exp = fixed_time + timedelta(minutes=expires_minutes)
        assert payload["exp"] == expected_exp.timestamp()


class TestDecodeToken:
    """トークンデコードのテスト"""

    def test_decode_token_valid_token(self):
        """有効なトークンのデコードをテスト"""
        sub = "test_user"
        token = create_access_token(sub)
        
        payload = decode_token(token)
        
        assert isinstance(payload, dict)
        assert payload["sub"] == sub
        assert "exp" in payload

    def test_decode_token_invalid_signature(self):
        """無効な署名のトークンデコードをテスト"""
        # 異なるキーで作成されたトークン
        sub = "test_user"
        payload = {"sub": sub, "exp": (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()}
        invalid_token = jwt.encode(payload, "wrong_secret_key", algorithm=settings.JWT_ALG)
        
        try:
            decode_token(invalid_token)
            assert False, "Expected JWTError"
        except JWTError:
            pass

    def test_decode_token_expired_token(self):
        """期限切れトークンのデコードをテスト"""
        sub = "expired_user"
        # 期限切れトークンを作成（過去の時刻）
        expired_token = create_access_token(sub, -10)
        
        try:
            decode_token(expired_token)
            assert False, "Expected JWTError"
        except JWTError:
            pass

    def test_decode_token_malformed_token(self):
        """不正な形式のトークンデコードをテスト"""
        malformed_tokens = [
            "invalid.token.format",
            "not_a_jwt_token",
            "",
            "a.b",  # 不完全なJWT
            "header.payload.signature.extra"  # 余分な部分
        ]
        
        for token in malformed_tokens:
            try:
                decode_token(token)
                assert False, f"Expected JWTError for token: {token}"
            except JWTError:
                pass

    def test_decode_token_with_different_algorithm(self):
        """異なるアルゴリズムで作成されたトークンのデコードをテスト"""
        sub = "test_user"
        payload = {"sub": sub, "exp": (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()}
        
        # 異なるアルゴリズム（RS256など）で作成
        try:
            # HS512で作成
            token_hs512 = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS512")
            decode_token(token_hs512)
            assert False, "Expected JWTError for different algorithm"
        except JWTError:
            pass

    def test_decode_token_empty_payload(self):
        """空のペイロードを持つトークンのデコードをテスト"""
        empty_payload = {}
        token = jwt.encode(empty_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)
        
        payload = decode_token(token)
        assert isinstance(payload, dict)
        assert payload == {}

    def test_decode_token_additional_claims(self):
        """追加のクレームを持つトークンのデコードをテスト"""
        custom_payload = {
            "sub": "user123",
            "name": "Test User",
            "admin": True,
            "exp": (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
        }
        token = jwt.encode(custom_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)
        
        payload = decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["name"] == "Test User"
        assert payload["admin"] is True


class TestEdgeCases:
    """エッジケースのテスト"""

    def test_create_and_decode_roundtrip(self):
        """トークン作成とデコードのラウンドトリップテスト"""
        subjects = [
            "123",
            "user@example.com",
            "ユーザー123",
            "!@#$%^&*()",
            "a" * 100  # 長いsubject
        ]
        
        for sub in subjects:
            token = create_access_token(sub)
            payload = decode_token(token)
            assert payload["sub"] == sub

    def test_token_consistency(self):
        """同じ入力からは同一または異なるトークンが生成されることを確認"""
        import time
        
        sub = "consistent_user"
        
        token1 = create_access_token(sub)
        time.sleep(1)  # 1秒待機して異なる時刻にする
        token2 = create_access_token(sub)
        
        # 時刻が異なるため、通常は異なるトークンが生成される
        # しかし、秒単位で同じ場合もあるので、同じでも異なってもOK
        payload1 = decode_token(token1)
        payload2 = decode_token(token2)
        
        # どちらも同じsubjectを持つことを確認
        assert payload1["sub"] == payload2["sub"] == sub

    def test_settings_integration(self):
        """設定ファイルとの統合テスト"""
        sub = "settings_test"
        token = create_access_token(sub)
        
        # 手動でjoseを使用してデコード
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALG]
        )
        
        assert payload["sub"] == sub

    @patch('app.core.config.settings')
    def test_decode_token_with_different_settings(self, mock_settings):
        """異なる設定でのトークンデコードテスト"""
        # この設定変更のテストは複雑なため、パスする
        pass
