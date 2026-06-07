from pathlib import Path
from typing import Optional

from models.source_models import LoadedSourceContent
from src.ingestion.base_loader import BaseLoader


class TextLoader(BaseLoader):
    """
    Loads plain text content from either:
    - a text string
    - a .txt file path
    """

    def __init__(
        self,
        source_id: str,
        title: str,
        text: Optional[str] = None,
        file_path: Optional[str] = None,
    ):
        super().__init__(source_id=source_id, title=title)
        self.text = text
        self.file_path = file_path

    def load(self) -> LoadedSourceContent:
        if self.text:
            content = self.text

        elif self.file_path:
            path = Path(self.file_path)

            if not path.exists():
                raise FileNotFoundError(f"Text file not found: {self.file_path}")

            content = path.read_text(encoding="utf-8")

        else:
            raise ValueError("Either text or file_path must be provided.")

        cleaned_text = self._clean_text(content)

        return LoadedSourceContent(
            user_id="temporary",
            source_id=self.source_id,
            source_type="text",
            title=self.title,
            text=cleaned_text,
            metadata={
                "character_count": len(cleaned_text)
            }
        )

    @staticmethod
    def _clean_text(text: str) -> str:
        return text.strip()