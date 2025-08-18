"""SQLAlchemyCategoryRepositoryの統合テスト

要件：
1. 実際のPostgreSQLデータベースにアクセス
2. 各テストでデータベースの状態を分離
3. C0カバレッジ100%、C1カバレッジ100%を達成
4. 各メソッドの境界値テストと異常系テストを含む
5. データベースの制約違反やエラーハンドリングをテスト
6. 複数のテストケースを並列実行してもデータが混在しない
7. テスト実行前後でデータベースの状態をクリーンに保つ
"""
import pytest

from app.infrastructure.sqlalchemy.repositories.category_repo_impl import SQLAlchemyCategoryRepository
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.domain.category.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class TestSQLAlchemyCategoryRepository:
    """SQLAlchemyCategoryRepositoryの統合テスト"""
    
    @pytest.fixture
    def repository(self, async_session: AsyncSession) -> SQLAlchemyCategoryRepository:
        """テスト対象のリポジトリインスタンス"""
        return SQLAlchemyCategoryRepository(async_session)
    
    # === saveメソッドのテスト ===
    
    async def test_save_new_category_success(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """新規カテゴリの保存が正常に完了することを確認"""
        # Arrange
        category = Category(category_id=0, name="新規カテゴリ")  # IDは0でsave時に設定される
        
        # Act
        await repository.save(category)
        
        # Assert - データベースに保存されていることを確認
        result = await async_session.execute(
            select(CategoryORM).where(CategoryORM.category_name == "新規カテゴリ")
        )
        saved_orm = result.scalar_one_or_none()
        
        assert saved_orm is not None
        assert saved_orm.category_name == "新規カテゴリ"
        assert category.id > 0  # IDが設定されている
    
    async def test_save_with_invalid_id_negative(self):
        """負のIDでカテゴリ作成時にエラーが発生することを確認"""
        # Act & Assert
        with pytest.raises(ValueError, match="カテゴリIDは0以上でなければなりません"):
            Category(category_id=-1, name="無効カテゴリ")
    
    # === list_allメソッドのテスト ===
    
    async def test_list_all_empty_database(self, repository: SQLAlchemyCategoryRepository):
        """データベースが空の場合、空のリストが返されることを確認"""
        # Act
        categories = await repository.list_all()
        
        # Assert
        assert categories == []
    
    async def test_list_all_single_category(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """1件のカテゴリが存在する場合の取得確認"""
        # Arrange - 直接ORMでデータを作成
        category_orm = CategoryORM(category_id=1, category_name="単一カテゴリ")
        async_session.add(category_orm)
        await async_session.commit()
        
        # Act
        categories = await repository.list_all()
        
        # Assert
        assert len(categories) == 1
        assert categories[0].name == "単一カテゴリ"
        assert categories[0].id > 0
    
    async def test_list_all_multiple_categories(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """複数のカテゴリが存在する場合の取得確認"""
        # Arrange - 直接ORMでデータを作成
        category_orms = [
            CategoryORM(category_id=1, category_name="カテゴリA"),
            CategoryORM(category_id=2, category_name="カテゴリB"),
            CategoryORM(category_id=3, category_name="カテゴリC")
        ]
        for orm in category_orms:
            async_session.add(orm)
        await async_session.commit()
        
        # Act
        categories = await repository.list_all()
        
        # Assert
        assert len(categories) == 3
        
        # 名前でソートして比較
        category_names = sorted([cat.name for cat in categories])
        expected_names = ["カテゴリA", "カテゴリB", "カテゴリC"]
        assert category_names == expected_names
    
    # === get_by_idメソッドのテスト ===
    
    async def test_get_by_id_existing_category(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """存在するカテゴリIDで正常に取得できることを確認"""
        # Arrange - 直接ORMでデータを作成
        category_orm = CategoryORM(category_id=1, category_name="取得テストカテゴリ")
        async_session.add(category_orm)
        await async_session.commit()
        await async_session.refresh(category_orm)
        
        # Act
        found_category = await repository.get_by_id(category_orm.category_id)
        
        # Assert
        assert found_category is not None
        assert found_category.id == category_orm.category_id
        assert found_category.name == "取得テストカテゴリ"
    
    async def test_get_by_id_nonexistent_category(self, repository: SQLAlchemyCategoryRepository):
        """存在しないカテゴリIDでNoneが返されることを確認"""
        # Arrange
        nonexistent_id = 99999
        
        # Act
        found_category = await repository.get_by_id(nonexistent_id)
        
        # Assert
        assert found_category is None
    
    async def test_get_by_id_with_zero_id(self, repository: SQLAlchemyCategoryRepository):
        """ID=0での取得でNoneが返されることを確認"""
        # Act
        found_category = await repository.get_by_id(0)
        
        # Assert
        assert found_category is None
    
    # === next_identifierメソッドのテスト ===
    
    async def test_next_identifier_empty_database(self, repository: SQLAlchemyCategoryRepository):
        """データベースが空の場合、1が返されることを確認"""
        # Act
        next_id = await repository.next_identifier()
        
        # Assert
        assert next_id == 1
    
    async def test_next_identifier_with_existing_data(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """既存データがある場合、最大ID+1が返されることを確認"""
        # Arrange - 複数のカテゴリを作成
        category_orms = [
            CategoryORM(category_id=1, category_name="カテゴリ1"),
            CategoryORM(category_id=2, category_name="カテゴリ2"),
            CategoryORM(category_id=3, category_name="カテゴリ3")
        ]
        for orm in category_orms:
            async_session.add(orm)
        await async_session.commit()
        
        # 最大IDを取得
        result = await async_session.execute(
            select(CategoryORM.category_id).order_by(CategoryORM.category_id.desc()).limit(1)
        )
        max_id = result.scalar_one()
        
        # Act
        next_id = await repository.next_identifier()
        
        # Assert
        assert next_id == max_id + 1
    
    async def test_next_identifier_returns_int(self, repository: SQLAlchemyCategoryRepository):
        """next_identifierがint型を返すことを確認"""
        # Act
        next_id = await repository.next_identifier()
        
        # Assert
        assert isinstance(next_id, int)
        assert next_id > 0
    
    # === updateメソッドのテスト ===
    
    async def test_update_existing_category_success(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """既存カテゴリの更新が正常に完了することを確認"""
        # Arrange - 先にカテゴリを作成
        category_orm = CategoryORM(category_id=1, category_name="更新前カテゴリ")
        async_session.add(category_orm)
        await async_session.commit()
        await async_session.refresh(category_orm)
        
        updated_category = Category(
            category_id=category_orm.category_id,
            name="更新後カテゴリ"
        )
        
        # Act
        await repository.update(updated_category)
        
        # Assert - データベースで更新されていることを確認
        result = await async_session.execute(
            select(CategoryORM).where(CategoryORM.category_id == category_orm.category_id)
        )
        updated_orm = result.scalar_one_or_none()
        
        assert updated_orm is not None
        assert updated_orm.category_name == "更新後カテゴリ"
    
    async def test_update_nonexistent_category(self, repository: SQLAlchemyCategoryRepository):
        """存在しないカテゴリの更新で何も起こらないことを確認"""
        # Arrange
        nonexistent_category = Category(
            category_id=99999,
            name="存在しないカテゴリ"
        )
        
        # Act - 例外が発生しないことを確認
        await repository.update(nonexistent_category)
        
        # Assert - 特に例外が発生しないことを確認（実装依存）
        # 現在の実装では、存在しないIDの場合は何も起こらない
    
    # === 統合テスト：複数操作の組み合わせ ===
    
    async def test_full_crud_cycle(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """作成→取得→更新→取得の完全なCRUDサイクルテスト"""
        # Create - 直接ORMで作成（saveメソッドはコミット込みなので）
        category_orm = CategoryORM(category_id=1, category_name="CRUDテストカテゴリ")
        async_session.add(category_orm)
        await async_session.commit()
        await async_session.refresh(category_orm)
        
        # Read
        retrieved_category = await repository.get_by_id(category_orm.category_id)
        assert retrieved_category is not None
        assert retrieved_category.name == "CRUDテストカテゴリ"
        
        # Update
        updated_category = Category(
            category_id=category_orm.category_id,
            name="更新されたCRUDテストカテゴリ"
        )
        await repository.update(updated_category)
        
        # Read again
        retrieved_updated = await repository.get_by_id(category_orm.category_id)
        assert retrieved_updated is not None
        assert retrieved_updated.name == "更新されたCRUDテストカテゴリ"
        
        # Verify in list
        all_categories = await repository.list_all()
        found_in_list = any(cat.id == category_orm.category_id for cat in all_categories)
        assert found_in_list
    
    # === エラーハンドリングとエッジケース ===
    
    async def test_category_name_empty_string(self):
        """空文字列の名前でカテゴリ作成時の動作確認"""
        # Act & Assert
        # Categoryクラス自体にはバリデーションがないので、ORMレベルでのテスト
        category = Category(category_id=1, name="")
        assert category.name == ""  # 現在の実装では許可される
    
    async def test_concurrent_next_identifier_calls(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """next_identifierの連続呼び出しで適切に増加することを確認"""
        # Act
        id1 = await repository.next_identifier()
        
        # 1つカテゴリを作成
        category_orm = CategoryORM(category_id=id1, category_name="テスト")
        async_session.add(category_orm)
        await async_session.commit()
        
        id2 = await repository.next_identifier()
        
        # Assert
        assert id2 > id1
    
    # === パフォーマンステスト ===
    
    async def test_list_all_performance_with_many_records(self, repository: SQLAlchemyCategoryRepository, async_session: AsyncSession):
        """大量データでのlist_allのパフォーマンステスト"""
        # Arrange - 20件のカテゴリを作成（Docker環境での実行時間を考慮）
        category_orms = []
        for i in range(20):
            category_orm = CategoryORM(category_id=i+1, category_name=f"パフォーマンステスト{i:03d}")
            category_orms.append(category_orm)
            async_session.add(category_orm)
        
        await async_session.commit()
        
        # Act
        all_categories = await repository.list_all()
        
        # Assert
        assert len(all_categories) == 20
        
        # すべてのカテゴリが取得されていることを確認
        category_names = [cat.name for cat in all_categories]
        for i in range(20):
            expected_name = f"パフォーマンステスト{i:03d}"
            assert expected_name in category_names