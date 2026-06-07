from abc import ABC, abstractmethod
from models.source_models import LoadedSourceContent


class BaseLoader(ABC):
    """
    Abstract base class for all loaders.

    Every loader (PDF, YouTube, Text) must implement `load`
    and return LoadedSourceContent.
    """

    def __init__(self, source_id: str, title: str):
        self.source_id = source_id
        self.title = title

    @abstractmethod
    def load(self) -> LoadedSourceContent:
        """
        Load and return normalized content.

        Must return:
        - full text
        - source metadata (optional)
        """
        pass