from typing import List, Optional, Dict, Any

from src.ingestion.embedders.gemini_embedder import GeminiEmbedder
from src.ingestion.indexers.faiss_indexer import FaissIndexer
from src.retrieval.keyword_retriever import KeywordRetriever


class Retriever:
    def __init__(self):
        self.embedder = GeminiEmbedder()
        test_embedding = self.embedder.embed_text("test")
        self.embedding_dim = len(test_embedding)

    def retrieve(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        source_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:

        indexer = FaissIndexer(
            embedding_dim=self.embedding_dim,
            user_id=user_id,
        )

        keyword = KeywordRetriever(
            user_id=user_id,
            embedding_dim=self.embedding_dim,
        )

        query_embedding = self.embedder.embed_text(query)

        semantic_results = indexer.search(
            query_embedding=query_embedding,
            top_k=top_k * 10,
        )

        keyword_results = keyword.retrieve(
            query=query,
            top_k=top_k * 10,
        )

        combined = semantic_results + keyword_results

        seen = set()
        unique_results = []

        for item in combined:
            metadata = item.get("metadata", {})
            chunk_id = metadata.get("chunk_id")

            if not chunk_id:
                continue

            if chunk_id in seen:
                continue

            seen.add(chunk_id)
            unique_results.append(item)

        filtered = []

        for item in unique_results:
            metadata = item.get("metadata", {})

            if metadata.get("user_id") != user_id:
                continue

            if source_ids and metadata.get("source_id") not in source_ids:
                continue

            filtered.append(item)

        return filtered[:top_k]