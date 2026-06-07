from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

from src.ingestion.indexers.faiss_indexer import FaissIndexer


class KeywordRetriever:
    """
    BM25 keyword-based retriever.
    Loads metadata from a user-specific FAISS index folder.
    """

    def __init__(self, user_id: str, embedding_dim: int):
        self.user_id = user_id
        self.indexer = FaissIndexer(
            embedding_dim=embedding_dim,
            user_id=user_id,
        )

        self.documents = []
        self.tokenized_docs = []
        self.bm25 = None

        self._load_documents()

    def _load_documents(self):
        metadata = self.indexer.metadata

        # Extra safety: only current user's chunks
        user_items = [
            item for item in metadata
            if item.get("metadata", {}).get("user_id") == self.user_id
        ]

        self.documents = [item["text"] for item in user_items]
        self.items = user_items

        self.tokenized_docs = [
            doc.lower().split()
            for doc in self.documents
        ]

        if self.tokenized_docs:
            self.bm25 = BM25Okapi(self.tokenized_docs)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.bm25:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:top_k]

        return [self.items[i] for i in ranked_indices]