# Category domain value objects
# app/domain/category/value_objects.py

class CategoryName:
    """カテゴリ名の値オブジェクト"""
    
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("カテゴリ名は空にできません")
        if len(value) > 100:
            raise ValueError("カテゴリ名は100文字以内である必要があります")
        self._value = value.strip()
    
    @property
    def value(self) -> str:
        return self._value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CategoryName):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __str__(self) -> str:
        return self._value
