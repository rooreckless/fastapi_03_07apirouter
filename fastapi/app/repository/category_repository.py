# ②抽象リポジトリクラス
# app/repository/category_repository.py
from abc import ABC, abstractmethod
from app.domain.entities.category import Category   #  ①のエンティティに依存

class CategoryRepository(ABC):
    @abstractmethod
    async def save(self, category: Category) -> None: ...
    @abstractmethod
    async def list_all(self) -> list[Category]: ...
