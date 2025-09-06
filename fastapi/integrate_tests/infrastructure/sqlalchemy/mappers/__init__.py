# Infrastructure層 - CategoryMapper 統合テスト
# CategoryMapperの統合テスト（データベースとの連携含む）
# 責務：
# - 実際のデータベースコンテキストでのMapper動作確認
# - ORMとマッパーの統合動作テスト

from app.infrastructure.sqlalchemy.mappers.category_mapper import CategoryMapper

# 統合テスト用のMappersテストはプレースホルダーとして作成
# 実際の統合テストは既存のrepo_implesテストで網羅されている

__all__ = ["CategoryMapper"]
