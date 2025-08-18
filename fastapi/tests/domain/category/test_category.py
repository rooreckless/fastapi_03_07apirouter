# fastapi/tests/domain/category/test_category.py

import pytest
# テスト対象のモジュールをインポート(fastapiからではなく、appから)
from app.domain.category.category import Category
# テスト対象モジュールが値オブジェクトを作成するのに必要なのでインポート
from app.domain.category.value_objects import CategoryName


# 正常系: 通常文字列
def test_create_category():
    name = CategoryName("  プログラミング ")
    assert name.value == "プログラミング"
    category = Category(category_id=1, name=name.value)
    assert category.name == "プログラミング"

# 異常系: カテゴリidが負の数の場合
def test_create_category_invalid_id():
    name = CategoryName("  プログラミング ")
    assert name.value == "プログラミング"

    with pytest.raises(ValueError, match="カテゴリIDは0以上でなければなりません"):
        Category(category_id=-1, name="Invalid Category")

# エッジケース: category_idが0のとき（ちょうど境界）
def test_create_category_id_zero():
    category = Category(category_id=0, name="Zero")
    assert category.id == 0
    assert category.name == "Zero"

# # エッジケース: nameが空文字列　← いらない 値オブジェクトの方であるから。
# def test_create_category_empty_name():
#     category = Category(category_id=10, name="")
#     assert category.name == ""

# 正常系: 100文字ちょうど
def test_create_category_name_max_length():
    long_name = "a" * 100
    name = CategoryName(long_name)
    assert name.value == long_name

# 正常系: __eq__ と __hash__
def test_category_name_equality_and_hash():
    a = CategoryName("AI")
    b = CategoryName("AI")
    c = CategoryName("ML")
    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)

# 異常系: 空文字列
def test_create_category_name_empty_string():
    with pytest.raises(ValueError, match="カテゴリ名は空にできません"):
        CategoryName("")

# 異常系: 空白のみ
def test_create_category_name_only_spaces():
    with pytest.raises(ValueError, match="カテゴリ名は空にできません"):
        CategoryName("     ")

# 異常系: 101文字
def test_create_category_name_too_long():
    too_long = "x" * 101
    with pytest.raises(ValueError, match="カテゴリ名は100文字以内である必要があります"):
        CategoryName(too_long)

# エッジケース: __eq__ に異なる型を渡す
def test_category_name_equality_with_different_type():
    name = CategoryName("Test")
    assert name != "Test"  # 異なる型との比較はFalse
