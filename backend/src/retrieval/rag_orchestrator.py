from typing import List, Optional

from src.retrieval.retriever import Retriever
from src.generation.generator import Generator


class RAGOrchestrator:
    """
    Coordinates:
    - query rewriting
    - retrieval
    - context building
    - LLM generation
    """

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def run(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        source_ids: Optional[List[str]] = None,
    ):
        rewritten_query = self.generator.rewrite_query(query)

        results = self.retriever.retrieve(
            query=rewritten_query,
            user_id=user_id,
            top_k=top_k,
            source_ids=source_ids,
        )

        if not results:
            return {
                "answer": "No relevant information found.",
                "sources": [],
                "rewritten_query": rewritten_query,
            }

        context = self._build_context(results)

        answer = self.generator.generate(
            query=query,
            context=context,
        )

        sources = self._format_sources(results)

        return {
            "answer": answer,
            "sources": sources,
            "rewritten_query": rewritten_query,
        }

    def _build_context(self, results) -> str:
        context_blocks = []

        for i, item in enumerate(results):
            text = item.get("text", "")

            context_blocks.append(
                f"[{i + 1}] {text}"
            )

        return "\n\n".join(context_blocks)

    def _format_sources(self, results):
        formatted = []

        for item in results:
            meta = item.get("metadata", {})

            formatted.append(
                {
                    "source_id": meta.get("source_id"),
                    "title": meta.get("title"),
                    "type": meta.get("source_type"),
                    "chunk_index": meta.get("chunk_index"),
                }
            )

        return formatted