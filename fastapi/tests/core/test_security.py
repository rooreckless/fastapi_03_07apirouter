# tests/core/test_security.py
"""
セキュリティ機能用のテストケース
"""
from unittest.mock import patch

from app.core.security import hash_password, verify_password, pwd_context


class TestHashPassword:
    """パスワードハッシュ化のテスト"""

    def test_hash_password_creates_bcrypt_hash(self):
        """パスワードが正しくbcryptでハッシュ化されることを確認"""
        password = "test_password123"
        hashed = hash_password(password)
        
        # bcryptハッシュの形式確認
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60  # bcryptハッシュの標準長
        
        # 同じパスワードでも異なるハッシュが生成されることを確認
        hashed2 = hash_password(password)
        assert hashed != hashed2

    def test_hash_password_with_empty_string(self):
        """空文字列のハッシュ化テスト"""
        password = ""
        hashed = hash_password(password)
        
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_special_characters(self):
        """特殊文字を含むパスワードのハッシュ化テスト"""
        password = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/"
        hashed = hash_password(password)
        
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_unicode_characters(self):
        """Unicode文字を含むパスワードのハッシュ化テスト"""
        password = "パスワード123こんにちは"
        hashed = hash_password(password)
        
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_long_password(self):
        """長いパスワードのハッシュ化テスト"""
        password = "a" * 1000  # 1000文字のパスワード
        hashed = hash_password(password)
        
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_context_integration(self):
        """pwd_contextとの統合テスト"""
        password = "test_password"
        hashed = hash_password(password)
        
        # pwd_contextで直接検証
        assert pwd_context.verify(password, hashed)


class TestVerifyPassword:
    """パスワード検証のテスト"""

    def test_verify_password_correct_password_returns_true(self):
        """正しいパスワードでTrueを返すテスト"""
        password = "correct_password"
        hashed = hash_password(password)
        
        result = verify_password(password, hashed)
        assert result is True

    def test_verify_password_incorrect_password_returns_false(self):
        """間違ったパスワードでFalseを返すテスト"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        result = verify_password(wrong_password, hashed)
        assert result is False

    def test_verify_password_empty_plain_password(self):
        """空の平文パスワードのテスト"""
        hashed = hash_password("some_password")
        
        result = verify_password("", hashed)
        assert result is False

    def test_verify_password_empty_hashed_password(self):
        """空のハッシュパスワードのテスト"""
        result = verify_password("password", "")
        assert result is False

    def test_verify_password_invalid_hash_format(self):
        """無効なハッシュ形式のテスト"""
        result = verify_password("password", "invalid_hash")
        assert result is False

    def test_verify_password_malformed_bcrypt_hash(self):
        """不正なbcryptハッシュのテスト"""
        result = verify_password("password", "$2b$12$invalid")
        assert result is False

    def test_verify_password_with_special_characters(self):
        """特殊文字を含むパスワードの検証テスト"""
        password = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password(password + "x", hashed) is False

    def test_verify_password_with_unicode_characters(self):
        """Unicode文字を含むパスワードの検証テスト"""
        password = "パスワード123こんにちは"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password(password + "x", hashed) is False

    def test_verify_password_case_sensitive(self):
        """大文字小文字の区別テスト"""
        password = "Password123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("password123", hashed) is False
        assert verify_password("PASSWORD123", hashed) is False

    def test_verify_password_exception_handling(self):
        """例外処理のテスト"""
        with patch.object(pwd_context, 'verify') as mock_verify:
            mock_verify.side_effect = Exception("Verification error")
            
            result = verify_password("password", "hash")
            assert result is False
            mock_verify.assert_called_once_with("password", "hash")

    def test_verify_password_various_exception_types(self):
        """さまざまな例外タイプの処理テスト"""
        test_cases = [
            ValueError("Invalid hash"),
            TypeError("Type error"),
            RuntimeError("Runtime error"),
            Exception("Generic error")
        ]
        
        for exception in test_cases:
            with patch.object(pwd_context, 'verify') as mock_verify:
                mock_verify.side_effect = exception
                
                result = verify_password("password", "hash")
                assert result is False


class TestPwdContext:
    """pwd_contextの設定テスト"""

    def test_pwd_context_configuration(self):
        """pwd_contextの設定が正しいことを確認"""
        assert "bcrypt" in pwd_context.schemes()
        # deprecatedは設定の内容ではなく、設定が適用されていることを確認
        assert pwd_context is not None

    def test_pwd_context_bcrypt_rounds(self):
        """bcryptのrounds設定をテスト"""
        # ハッシュを生成して形式を確認
        password = "test"
        hashed = pwd_context.hash(password)
        
        # bcryptのrounds=12の場合、$2b$12$で始まる
        assert hashed.startswith("$2b$12$")

    def test_pwd_context_hash_and_verify_integration(self):
        """pwd_contextのhashとverifyの統合テスト"""
        password = "integration_test"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify(password, hashed)
        assert not pwd_context.verify("wrong", hashed)


class TestEdgeCases:
    """エッジケースのテスト"""

    def test_verify_password_none_values(self):
        """None値の処理テスト"""
        # pwd_contextがNone値をどう処理するかによって結果が変わるが、
        # 通常は例外が発生してFalseになることを期待
        result = verify_password(None, "hash")
        assert result is False

    def test_hash_password_very_long_input(self):
        """非常に長い入力のテスト（制限内）"""
        # passlibの制限内の長さでテスト（通常4096バイト以下）
        long_password = "a" * 4000
        hashed = hash_password(long_password)
        
        assert isinstance(hashed, str)
        assert verify_password(long_password, hashed)

    def test_hash_password_exceeds_size_limit(self):
        """サイズ制限を超えるパスワードのテスト"""
        from passlib.exc import PasswordSizeError
        
        # 制限を超える長さ（10000文字）
        very_long_password = "a" * 10000
        
        try:
            hash_password(very_long_password)
            # 例外が発生しなかった場合はテスト失敗
            assert False, "Expected PasswordSizeError"
        except PasswordSizeError:
            # 期待される例外
            pass

    def test_verify_password_with_console_output(self):
        """コンソール出力が含まれる例外処理のテスト"""
        with patch.object(pwd_context, 'verify') as mock_verify, \
             patch('builtins.print') as mock_print:
            
            mock_verify.side_effect = Exception("Test error")
            
            result = verify_password("password", "hash")
            
            assert result is False
            mock_print.assert_called_once_with("Password verification error: Test error")

    def test_hash_password_deterministic_behavior(self):
        """ハッシュ化の非決定的動作の確認"""
        password = "test_deterministic"
        
        # 同じパスワードから複数のハッシュを生成
        hashes = [hash_password(password) for _ in range(5)]
        
        # すべて異なるハッシュが生成されることを確認
        assert len(set(hashes)) == 5
        
        # すべてのハッシュが元のパスワードで検証できることを確認
        for hashed in hashes:
            assert verify_password(password, hashed)
