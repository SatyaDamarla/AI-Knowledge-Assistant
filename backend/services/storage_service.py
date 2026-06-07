from pathlib import Path
from typing import Tuple
import uuid


class StorageService:
    """
    Handles all file system storage:
    - uploaded files (PDF)
    - normalized text
    - transcripts
    """

    BASE_PATH = Path("data")

    DOCS_PATH = BASE_PATH / "docs"
    TRANSCRIPTS_PATH = BASE_PATH / "transcripts"
    NOTES_PATH = BASE_PATH / "notes"
    NORMALIZED_PATH = BASE_PATH / "normalized"

    @classmethod
    def _ensure_dirs(cls):
        cls.DOCS_PATH.mkdir(parents=True, exist_ok=True)
        cls.TRANSCRIPTS_PATH.mkdir(parents=True, exist_ok=True)
        cls.NOTES_PATH.mkdir(parents=True, exist_ok=True)
        cls.NORMALIZED_PATH.mkdir(parents=True, exist_ok=True)

    # -------- FILE STORAGE --------

    @classmethod
    def save_uploaded_file(cls, file) -> Tuple[str, str]:
        """
        Save uploaded file (PDF)
        Returns: (source_id, file_path)
        """
        cls._ensure_dirs()

        source_id = f"src_{uuid.uuid4().hex[:8]}"
        filename = file.filename.replace(" ", "_")

        file_path = cls.DOCS_PATH / f"{source_id}_{filename}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return source_id, str(file_path)

    # -------- TEXT STORAGE --------

    @classmethod
    def save_text(cls, source_id: str, text: str, source_type: str) -> str:
        """
        Save raw text (YouTube / pasted text)
        Returns path to saved file
        """
        cls._ensure_dirs()

        if source_type == "youtube":
            path = cls.TRANSCRIPTS_PATH / f"{source_id}.txt"
        else:
            path = cls.NOTES_PATH / f"{source_id}.txt"

        path.write_text(text, encoding="utf-8")

        return str(path)

    # -------- NORMALIZED TEXT --------

    @classmethod
    def save_normalized_text(cls, source_id: str, text: str) -> str:
        """
        Save cleaned/processed text for chunking
        """
        cls._ensure_dirs()

        path = cls.NORMALIZED_PATH / f"{source_id}.txt"
        path.write_text(text, encoding="utf-8")

        return str(path)