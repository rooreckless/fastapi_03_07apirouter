"""
item_repo_impl.pyのためのテストモジュール

SQLAlchemyItemRepositoryクラスの全メソッドを対象として
PostgreSQLとの実際の統合を含む包括的なテストを実施
"""
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.sqlalchemy.repositories.item_repo_impl import SQLAlchemyItemRepository
from app.infrastructure.sqlalchemy.models.item_orm import ItemORM
from app.infrastructure.sqlalchemy.models.category_orm import CategoryORM
from app.domain.items.item import Item


class TestSQLAlchemyItemRepository:
    """SQLAlchemyItemRepositoryのテストクラス"""
    
    @pytest.fixture
    def repository(self, async_session: AsyncSession) -> SQLAlchemyItemRepository:
        """テスト対象のリポジトリインスタンス"""
        return SQLAlchemyItemRepository(async_session)

    # === saveメソッドのテスト ===
    
    async def test_save_item_with_no_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: カテゴリが空のアイテムを保存する
        """
        # Arrange
        item = Item(item_id=1, name="Test Item", category_ids=[])
        
        # Act
        await repository.save(item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one_or_none()
        
        assert saved_item is not None
        assert saved_item.item_name == "Test Item"
        
        # カテゴリの関連を確認（遅延ロードを避けて直接クエリ）
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 0

    async def test_save_item_with_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: カテゴリ付きのアイテムを保存する
        """
        # Arrange - カテゴリを事前作成
        category1 = CategoryORM(category_id=1, category_name="Category 1")
        category2 = CategoryORM(category_id=2, category_name="Category 2")
        async_session.add_all([category1, category2])
        await async_session.commit()
        
        item = Item(item_id=1, name="Item with Categories", category_ids=[1, 2])
        
        # Act
        await repository.save(item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one_or_none()
        
        assert saved_item is not None
        assert saved_item.item_name == "Item with Categories"
        
        # カテゴリの関連を確認
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
            .order_by(CategoryORM.category_id)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 2
        assert categories[0].category_id == 1
        assert categories[1].category_id == 2

    # === list_allメソッドのテスト ===
    
    async def test_list_all_empty_database(self, repository: SQLAlchemyItemRepository):
        """
        エッジケース: データベースが空の場合の一覧取得
        """
        # Act
        items = await repository.list_all()
        
        # Assert
        assert items == []

    async def test_list_all_with_items(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: アイテム一覧の取得
        """
        # Arrange
        category = CategoryORM(category_id=1, category_name="Test Category")
        item1 = ItemORM(item_id=1, item_name="Item 1", categories=[category])
        item2 = ItemORM(item_id=2, item_name="Item 2", categories=[])
        
        async_session.add_all([category, item1, item2])
        await async_session.commit()
        
        # Act
        items = await repository.list_all()
        
        # Assert
        assert len(items) == 2
        
        items_by_id = {item.id: item for item in items}
        
        assert items_by_id[1].name == "Item 1"
        assert items_by_id[1].category_ids == [1]
        
        assert items_by_id[2].name == "Item 2"
        assert items_by_id[2].category_ids == []

    # === get_by_idメソッドのテスト ===
    
    async def test_get_by_id_existing_item(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 存在するアイテムの詳細取得
        """
        # Arrange
        category = CategoryORM(category_id=1, category_name="Test Category")
        item = ItemORM(item_id=1, item_name="Test Item", categories=[category])
        
        async_session.add_all([category, item])
        await async_session.commit()
        
        # Act
        result = await repository.get_by_id(1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Item"
        assert result.category_ids == [1]

    async def test_get_by_id_nonexistent_item(self, repository: SQLAlchemyItemRepository):
        """
        正常系: 存在しないアイテムの詳細取得（None が返される）
        """
        # Act
        result = await repository.get_by_id(999)
        
        # Assert
        assert result is None

    # === next_identifierメソッドのテスト ===
    
    async def test_next_identifier_empty_database(self, repository: SQLAlchemyItemRepository):
        """
        エッジケース: データベースが空の場合のID生成
        """
        # Act
        next_id = await repository.next_identifier()
        
        # Assert
        assert next_id == 1

    async def test_next_identifier_with_existing_items(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 既存アイテムがある場合のID生成
        """
        # Arrange
        item1 = ItemORM(item_id=1, item_name="Item 1")
        item2 = ItemORM(item_id=5, item_name="Item 5")
        
        async_session.add_all([item1, item2])
        await async_session.commit()
        
        # Act
        next_id = await repository.next_identifier()
        
        # Assert - 最大ID=5の次なので6
        assert next_id == 6

    # === updateメソッドのテスト ===
    
    async def test_update_existing_item_name_only(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 既存アイテムの名前のみ更新
        """
        # Arrange
        item_orm = ItemORM(item_id=1, item_name="Original Name")
        async_session.add(item_orm)
        await async_session.commit()
        
        updated_item = Item(item_id=1, name="Updated Name", category_ids=[])
        
        # Act
        await repository.update(updated_item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one()
        assert saved_item.item_name == "Updated Name"

    # === deleteメソッドのテスト ===
    
    async def test_delete_existing_item(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 既存アイテムの削除
        """
        # Arrange
        item = ItemORM(item_id=1, item_name="Test Item")
        async_session.add(item)
        await async_session.commit()
        
        # Act
        await repository.delete(1)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        deleted_item = result.scalar_one_or_none()
        assert deleted_item is None

    async def test_delete_nonexistent_item(self, repository: SQLAlchemyItemRepository):
        """
        異常系: 存在しないアイテムの削除でValueError例外発生
        """
        # Act & Assert
        with pytest.raises(ValueError, match="Item with ID 999 not found."):
            await repository.delete(999)

    async def test_update_existing_item_with_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 既存アイテムのカテゴリを更新
        """
        # Arrange
        category1 = CategoryORM(category_id=1, category_name="Category 1")
        category2 = CategoryORM(category_id=2, category_name="Category 2")
        item_orm = ItemORM(item_id=1, item_name="Test Item", categories=[category1])
        
        async_session.add_all([category1, category2, item_orm])
        await async_session.commit()
        
        updated_item = Item(item_id=1, name="Updated Item", category_ids=[2])
        
        # Act
        await repository.update(updated_item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one()
        assert saved_item.item_name == "Updated Item"
        
        # カテゴリの関連を確認
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 1
        assert categories[0].category_id == 2
        # エンティティ状態も正しく更新されているか確認
        assert updated_item.category_ids == [2]

    async def test_update_remove_all_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 既存アイテムのカテゴリをすべて削除
        """
        # Arrange
        category = CategoryORM(category_id=1, category_name="Category 1")
        item_orm = ItemORM(item_id=1, item_name="Test Item", categories=[category])
        
        async_session.add_all([category, item_orm])
        await async_session.commit()
        
        updated_item = Item(item_id=1, name="Updated Item", category_ids=[])
        
        # Act
        await repository.update(updated_item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one()
        assert saved_item.item_name == "Updated Item"
        
        # カテゴリの関連を確認
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 0
        assert updated_item.category_ids == []

    async def test_update_with_none_category_ids(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        エッジケース: category_ids=Noneでアイテム更新
        """
        # Arrange
        category = CategoryORM(category_id=1, category_name="Category 1")
        item_orm = ItemORM(item_id=1, item_name="Test Item", categories=[category])
        
        async_session.add_all([category, item_orm])
        await async_session.commit()
        
        updated_item = Item(item_id=1, name="Updated Item", category_ids=None)
        
        # Act
        await repository.update(updated_item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one()
        assert saved_item.item_name == "Updated Item"
        
        # カテゴリの関連を確認
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 0
        assert updated_item.category_ids == []

    async def test_update_nonexistent_item(self, repository: SQLAlchemyItemRepository):
        """
        エッジケース: 存在しないアイテムの更新（何もせず正常終了）
        """
        # Arrange
        updated_item = Item(item_id=999, name="Nonexistent Item", category_ids=[])
        
        # Act（例外が発生しないことを確認）
        await repository.update(updated_item)
        # 何も変更されていないことが想定される動作

    async def test_delete_item_with_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: カテゴリ付きアイテムの削除（関連も正しく削除される）
        """
        # Arrange
        category = CategoryORM(category_id=1, category_name="Test Category")
        item = ItemORM(item_id=1, item_name="Test Item", categories=[category])
        
        async_session.add_all([category, item])
        await async_session.commit()
        
        # Act
        await repository.delete(1)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        deleted_item = result.scalar_one_or_none()
        assert deleted_item is None
        
        # カテゴリは残っていることを確認
        category_result = await async_session.execute(
            select(CategoryORM).where(CategoryORM.category_id == 1)
        )
        remaining_category = category_result.scalar_one_or_none()
        assert remaining_category is not None

    async def test_update_with_partial_category_matches(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        エッジケース: 一部のカテゴリが存在しない場合の更新
        """
        # Arrange
        category1 = CategoryORM(category_id=1, category_name="Category 1")
        # category_id=2は作成しない
        item_orm = ItemORM(item_id=1, item_name="Test Item")
        
        async_session.add_all([category1, item_orm])
        await async_session.commit()
        
        updated_item = Item(item_id=1, name="Updated Item", category_ids=[1, 2])
        
        # Act
        await repository.update(updated_item)
        
        # Assert
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one()
        
        # カテゴリの関連を確認（存在するカテゴリのみ設定される）
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 1
        assert categories[0].category_id == 1
        # エンティティ状態は実際に設定されたカテゴリを反映
        assert updated_item.category_ids == [1]

    # === 統合テスト ===
    
    async def test_integration_save_update_delete_flow(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 保存→更新→削除の一連の統合フロー
        """
        # Arrange - カテゴリの事前準備
        category = CategoryORM(category_id=1, category_name="Test Category")
        async_session.add(category)
        await async_session.commit()
        
        # Act & Assert - 1. 保存
        item = Item(item_id=1, name="Integration Test Item", category_ids=[1])
        await repository.save(item)
        
        saved_id = item.id
        assert saved_id == 1
        
        # 2. 取得確認
        retrieved_item = await repository.get_by_id(saved_id)
        assert retrieved_item is not None
        assert retrieved_item.name == "Integration Test Item"
        assert retrieved_item.category_ids == [1]
        
        # 3. 更新
        retrieved_item.name = "Updated Integration Test Item"
        retrieved_item.category_ids = []
        await repository.update(retrieved_item)
        
        # 更新確認
        updated_item = await repository.get_by_id(saved_id)
        assert updated_item.name == "Updated Integration Test Item"
        assert updated_item.category_ids == []
        
        # 4. 削除
        await repository.delete(saved_id)
        
        # 削除確認
        deleted_item = await repository.get_by_id(saved_id)
        assert deleted_item is None

    async def test_save_item_with_nonexistent_categories(self, repository: SQLAlchemyItemRepository, async_session: AsyncSession):
        """
        正常系: 存在しないカテゴリIDを含むアイテムを保存（カテゴリは無視される）
        """
        # Arrange
        item = Item(item_id=1, name="Item with Nonexistent Categories", category_ids=[999])
        
        # Act
        await repository.save(item)
        
        # Assert - 存在しないカテゴリは無視される
        result = await async_session.execute(
            select(ItemORM).where(ItemORM.item_id == 1)
        )
        saved_item = result.scalar_one_or_none()
        
        assert saved_item is not None
        assert saved_item.item_name == "Item with Nonexistent Categories"
        
        # カテゴリの関連を確認
        category_result = await async_session.execute(
            select(CategoryORM)
            .join(ItemORM.categories)
            .where(ItemORM.item_id == 1)
        )
        categories = category_result.scalars().all()
        assert len(categories) == 0

    async def test_concurrent_next_identifier_calls(self, repository: SQLAlchemyItemRepository):
        """
        エッジケース: next_identifierの複数回呼び出し（データベース状態が変わらない限り同じ値）
        """
        # Act - メソッド実行（複数回）
        id1 = await repository.next_identifier()
        id2 = await repository.next_identifier()
        
        # Assert - データベース状態が変わっていないので同じ値
        assert id1 == id2 == 1

    async def test_save_and_id_assignment(self, repository: SQLAlchemyItemRepository):
        """
        エッジケース: saveメソッドでIDが正しく設定されることを確認
        """
        # Arrange
        item = Item(item_id=1, name="Test Item", category_ids=[])
        original_id = item.id
        
        # Act
        await repository.save(item)
        
        # Assert - IDが同じままであることを確認
        assert item.id == original_id
        assert item.id == 1
