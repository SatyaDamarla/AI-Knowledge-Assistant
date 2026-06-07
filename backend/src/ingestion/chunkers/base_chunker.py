from abc import ABC, abstractmethod
from typing import List

from models.source_models import LoadedSourceContent, ChunkRecord


class BaseChunker(ABC):
    """
    Abstract base class for all chunking strategies.
    Every chunker must convert LoadedSourceContent -> List[ChunkRecord].
    """

    @abstractmethod
    def chunk(self, source: LoadedSourceContent) -> List[ChunkRecord]:
        pass