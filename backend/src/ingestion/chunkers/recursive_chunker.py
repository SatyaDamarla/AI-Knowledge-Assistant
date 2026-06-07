import uuid
from typing import List

from models.source_models import LoadedSourceContent, ChunkRecord
from src.ingestion.chunkers.base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):
    """
    Simple recursive-style text chunker.
    Splits large text into overlapping chunks.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, source: LoadedSourceContent) -> List[ChunkRecord]:
        text = source.text.strip()

        if not text:
            return []

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    ChunkRecord(
                        user_id=source.user_id,
                        chunk_id=f"chk_{uuid.uuid4().hex[:10]}",
                        source_id=source.source_id,
                        source_type=source.source_type,
                        title=source.title,
                        chunk_index=chunk_index,
                        text=chunk_text,
                        metadata={
                            **source.metadata,
                            "user_id": source.user_id,
                            "chunk_size": len(chunk_text),
                        },
                    )
                )

                chunk_index += 1

            start += self.chunk_size - self.chunk_overlap

        return chunks