# Items domain value objects
# app/domain/items/value_objects.py

class ItemName:
    """アイテム名の値オブジェクト"""
    
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("アイテム名は空にできません")
        if len(value) > 200:
            raise ValueError("アイテム名は200文字以内である必要があります")
        self._value = value.strip()
    
    @property
    def value(self) -> str:
        return self._value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ItemName):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __str__(self) -> str:
        return self._value


class CategoryId:
    """カテゴリIDの値オブジェクト"""
    
    def __init__(self, value: int):
        if value <= 0:
            raise ValueError("カテゴリIDは正の整数である必要があります")
        self._value = value
    
    @property
    def value(self) -> int:
        return self._value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CategoryId):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __str__(self) -> str:
        return str(self._value)
