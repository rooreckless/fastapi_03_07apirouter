# Category ID value object
# app/domain/items/value_objects/category_id.py

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
