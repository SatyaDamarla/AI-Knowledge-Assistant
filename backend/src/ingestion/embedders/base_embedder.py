from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    """
    Converts text chunks into embedding vectors.
    """

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass