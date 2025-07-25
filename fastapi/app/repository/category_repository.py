# ②抽象リポジトリクラス
# app/repository/category_repository.py
from abc import ABC, abstractmethod
from app.domain.category import Category   # ①のエンティティに依存

class CategoryRepository(ABC):
    @abstractmethod
    async def save(self, category: Category) -> None: ...
    @abstractmethod
    async def list_all(self) -> list[Category]: ...
    @abstractmethod
    async def get_by_id(self, category_id: int) -> Category | None: ...
    @abstractmethod
    async def next_identifier(self) -> int: ...
    @abstractmethod
    async def update(self, category: Category) -> None: ...