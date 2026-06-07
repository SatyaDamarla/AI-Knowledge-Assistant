from pathlib import Path
import fitz  # PyMuPDF

from models.source_models import LoadedSourceContent
from src.ingestion.base_loader import BaseLoader


class PDFLoader(BaseLoader):
    """
    Loads and extracts text from a PDF file.
    """

    def __init__(self, source_id: str, title: str, file_path: str):
        super().__init__(source_id=source_id, title=title)
        self.file_path = file_path

    def load(self) -> LoadedSourceContent:
        path = Path(self.file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {self.file_path}")

        doc = fitz.open(path)

        full_text = []
        page_texts = []

        for page_number, page in enumerate(doc):
            text = page.get_text()
            cleaned = self._clean_text(text)

            full_text.append(cleaned)

            page_texts.append({
                "page": page_number + 1,
                "text": cleaned
            })

        combined_text = "\n\n".join(full_text)

        return LoadedSourceContent(
            user_id="temporary",
            source_id=self.source_id,
            source_type="pdf",
            title=self.title,
            text=combined_text,
            metadata={
                "page_count": len(doc),
                "pages": page_texts  # useful later for chunk-level metadata
            }
        )

    @staticmethod
    def _clean_text(text: str) -> str:
        return text.strip()