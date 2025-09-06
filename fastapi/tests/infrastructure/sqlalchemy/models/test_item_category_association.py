"""Item Category Association テストモジュール."""

from sqlalchemy import Table, Column, Integer
from app.infrastructure.sqlalchemy.models.item_category_association import item_category
from app.db.base import Base


class TestItemCategoryAssociation:
    """item_category中間テーブルのテストクラス."""

    def test_item_category_table_exists(self):
        """正常系: item_categoryテーブルが存在する."""
        assert item_category is not None
        assert isinstance(item_category, Table)

    def test_item_category_table_name(self):
        """正常系: テーブル名が正しく設定される."""
        assert item_category.name == "item_category"

    def test_item_category_table_metadata(self):
        """正常系: テーブルのメタデータが正しく設定される."""
        assert item_category.metadata is Base.metadata

    def test_item_category_has_item_id_column(self):
        """正常系: item_idカラムが存在する."""
        columns = {col.name: col for col in item_category.columns}
        assert "item_id" in columns
        
        item_id_col = columns["item_id"]
        assert isinstance(item_id_col, Column)
        assert isinstance(item_id_col.type, Integer)
        assert item_id_col.primary_key is True

    def test_item_category_has_category_id_column(self):
        """正常系: category_idカラムが存在する."""
        columns = {col.name: col for col in item_category.columns}
        assert "category_id" in columns
        
        category_id_col = columns["category_id"]
        assert isinstance(category_id_col, Column)
        assert isinstance(category_id_col.type, Integer)
        assert category_id_col.primary_key is True

    def test_item_category_column_count(self):
        """正常系: カラム数が正しい."""
        assert len(item_category.columns) == 2

    def test_item_category_primary_key_columns(self):
        """正常系: 主キーが複合キーである."""
        primary_key_columns = [col for col in item_category.columns if col.primary_key]
        assert len(primary_key_columns) == 2
        
        pk_names = {col.name for col in primary_key_columns}
        assert pk_names == {"item_id", "category_id"}

    def test_item_category_foreign_key_constraints(self):
        """正常系: 外部キー制約が正しく設定される."""
        columns = {col.name: col for col in item_category.columns}
        
        # item_idの外部キー制約を確認
        item_id_col = columns["item_id"]
        item_id_fks = list(item_id_col.foreign_keys)
        assert len(item_id_fks) == 1
        assert str(item_id_fks[0].column) == "items.item_id"
        assert item_id_fks[0].ondelete == "CASCADE"
        
        # category_idの外部キー制約を確認
        category_id_col = columns["category_id"]
        category_id_fks = list(category_id_col.foreign_keys)
        assert len(category_id_fks) == 1
        assert str(category_id_fks[0].column) == "categories.category_id"
        assert category_id_fks[0].ondelete == "CASCADE"

    def test_item_category_table_structure(self):
        """正常系: テーブル構造が期待通りである."""
        assert item_category.name == "item_category"
        assert len(item_category.columns) == 2
        assert len(item_category.primary_key.columns) == 2

    def test_item_category_columns_data_types(self):
        """正常系: カラムのデータ型が正しい."""
        columns = {col.name: col for col in item_category.columns}
        
        item_id_col = columns["item_id"]
        category_id_col = columns["category_id"]
        
        assert isinstance(item_id_col.type, Integer)
        assert isinstance(category_id_col.type, Integer)

    def test_item_category_columns_nullable(self):
        """正常系: カラムのNULL制約が正しい."""
        columns = {col.name: col for col in item_category.columns}
        
        item_id_col = columns["item_id"]
        category_id_col = columns["category_id"]
        
        # 主キーカラムは通常NOT NULLになる
        assert item_id_col.nullable is False
        assert category_id_col.nullable is False

    def test_item_category_table_equality(self):
        """正常系: 同じテーブルオブジェクトが参照される."""
        # 再度インポートして同じオブジェクトが参照されることを確認
        from app.infrastructure.sqlalchemy.models.item_category_association import item_category as imported_table
        assert item_category is imported_table

    def test_item_category_table_representation(self):
        """正常系: テーブルの文字列表現が取得できる."""
        table_repr = repr(item_category)
        assert isinstance(table_repr, str)
        assert "item_category" in table_repr

    def test_item_category_table_str(self):
        """正常系: テーブルの文字列が取得できる."""
        table_str = str(item_category)
        assert isinstance(table_str, str)
        assert len(table_str) > 0

    def test_item_category_column_access(self):
        """正常系: カラムにアクセスできる."""
        # c属性を使ってカラムにアクセス
        assert hasattr(item_category.c, 'item_id')
        assert hasattr(item_category.c, 'category_id')
        
        # カラムオブジェクトが取得できる
        item_id_col = item_category.c.item_id
        category_id_col = item_category.c.category_id
        
        assert item_id_col.name == "item_id"
        assert category_id_col.name == "category_id"

    def test_item_category_column_iteration(self):
        """正常系: カラムを反復処理できる."""
        column_names = []
        for column in item_category.columns:
            column_names.append(column.name)
        
        assert len(column_names) == 2
        assert "item_id" in column_names
        assert "category_id" in column_names

    def test_item_category_table_info(self):
        """正常系: テーブル情報が取得できる."""
        # テーブル名
        assert item_category.name == "item_category"
        
        # スキーマ情報（デフォルトはNone）
        assert item_category.schema is None
        
        # メタデータ
        assert item_category.metadata is not None

    def test_item_category_foreign_key_references(self):
        """正常系: 外部キーが正しいテーブルを参照している."""
        columns = {col.name: col for col in item_category.columns}
        
        # item_idの外部キー参照先を確認
        item_id_col = columns["item_id"]
        for fk in item_id_col.foreign_keys:
            assert fk.column.table.name == "items"
            assert fk.column.name == "item_id"
        
        # category_idの外部キー参照先を確認
        category_id_col = columns["category_id"]
        for fk in category_id_col.foreign_keys:
            assert fk.column.table.name == "categories"
            assert fk.column.name == "category_id"

    def test_item_category_cascade_behavior(self):
        """正常系: CASCADE削除が設定されている."""
        columns = {col.name: col for col in item_category.columns}
        
        # 各カラムの外部キー制約でCASCADE削除が設定されていることを確認
        item_id_col = columns["item_id"]
        for fk in item_id_col.foreign_keys:
            assert fk.ondelete == "CASCADE"
        
        category_id_col = columns["category_id"]
        for fk in category_id_col.foreign_keys:
            assert fk.ondelete == "CASCADE"

    def test_item_category_table_in_metadata(self):
        """正常系: テーブルがメタデータに登録されている."""
        assert "item_category" in Base.metadata.tables
        registered_table = Base.metadata.tables["item_category"]
        assert registered_table is item_category

    def test_item_category_column_attributes(self):
        """正常系: カラムの属性が正しく設定されている."""
        columns = {col.name: col for col in item_category.columns}
        
        for col_name, col in columns.items():
            # カラム名が正しい
            assert col.name == col_name
            
            # 型がIntegerである
            assert isinstance(col.type, Integer)
            
            # 主キーである
            assert col.primary_key is True
            
            # NOT NULLである
            assert col.nullable is False
            
            # 外部キー制約が存在する
            assert len(list(col.foreign_keys)) == 1

    def test_item_category_table_hashable(self):
        """正常系: テーブルオブジェクトがハッシュ化可能である."""
        # テーブルオブジェクトがハッシュ化できることを確認
        hash_value = hash(item_category)
        assert isinstance(hash_value, int)

    def test_item_category_table_comparable(self):
        """正常系: テーブルオブジェクトが比較可能である."""
        # 同じテーブルオブジェクトとの比較
        assert item_category == item_category
        
        # 異なるオブジェクトとの比較（エラーが発生しないことを確認）
        assert item_category != "not_a_table"
