# ②抽象リポジトリクラス
# app/repository/item_repository.py
from abc import ABC, abstractmethod
from app.domain.entities.item import Item    #  ①のエンティティに依存

class ItemRepository(ABC):
    @abstractmethod
    async def save(self, item: Item) -> None: ...
    @abstractmethod
    async def list_all(self) -> list[Item]: ...
