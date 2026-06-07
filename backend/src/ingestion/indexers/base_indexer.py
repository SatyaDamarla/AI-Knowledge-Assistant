from abc import ABC, abstractmethod
from typing import List, Any

from models.source_models import ChunkRecord


class BaseIndexer(ABC):
    @abstractmethod
    def add(self, chunks: List[ChunkRecord], embeddings: List[List[float]]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Any]:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass