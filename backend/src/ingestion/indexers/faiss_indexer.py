import json
from pathlib import Path
from typing import List, Dict, Any

import faiss
import numpy as np

from models.source_models import ChunkRecord
from src.ingestion.indexers.base_indexer import BaseIndexer


class FaissIndexer(BaseIndexer):
    

    def __init__(self, embedding_dim: int, user_id: str):
        self.embedding_dim = embedding_dim
        self.user_id = user_id

        base_path = Path(f"data/vector_store/{user_id}")

        self.INDEX_PATH = base_path / "index.faiss"
        self.META_PATH = base_path / "index_meta.json"

        self.index = None
        self.metadata = []

        self._ensure_dirs()
        self.load()

    def _ensure_dirs(self) -> None:
        self.INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    def add(self, chunks: List[ChunkRecord], embeddings: List[List[float]]) -> None:
        if not chunks or not embeddings:
            return

        vectors = np.array(embeddings).astype("float32")

        if vectors.shape[1] != self.embedding_dim:
            raise ValueError(
                f"Embedding dimension mismatch. "
                f"Expected {self.embedding_dim}, got {vectors.shape[1]}"
            )

        if self.index is None:
            self.index = faiss.IndexFlatL2(self.embedding_dim)

        start_id = len(self.metadata)

        self.index.add(vectors)

        for i, chunk in enumerate(chunks):
            self.metadata.append(
                {
                    "faiss_id": start_id + i,
                    "text": chunk.text,
                    "metadata": {
                        "user_id": chunk.user_id,
                        "chunk_id": chunk.chunk_id,
                        "source_id": chunk.source_id,
                        "source_type": chunk.source_type,
                        "title": chunk.title,
                        "chunk_index": chunk.chunk_index,
                        **chunk.metadata,
                    },
                }
            )

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index is None or not self.metadata:
            return []

        query = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query, top_k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            if idx < len(self.metadata):
                item = self.metadata[idx].copy()
                item["score"] = float(distance)
                results.append(item)

        return results

    def save(self) -> None:
        self._ensure_dirs()

        if self.index is not None:
            faiss.write_index(self.index, str(self.INDEX_PATH))

        self.META_PATH.write_text(
            json.dumps(self.metadata, indent=2),
            encoding="utf-8",
        )

    def load(self) -> None:
        if self.INDEX_PATH.exists():
            self.index = faiss.read_index(str(self.INDEX_PATH))
        else:
            self.index = None

        if self.META_PATH.exists():
            raw = self.META_PATH.read_text(encoding="utf-8").strip()
            self.metadata = json.loads(raw) if raw else []
        else:
            self.metadata = []