from typing import List, Optional, Dict, Any

from src.retrieval.rag_orchestrator import RAGOrchestrator


class QueryService:
    """
    Application layer for handling user queries.
    """

    def __init__(self):
        self.rag = RAGOrchestrator()

    def query(
        self,
        question: str,
        user_id: str,
        source_ids: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:

        result = self.rag.run(
            query=question,
            user_id=user_id,
            top_k=top_k,
            source_ids=source_ids,
        )

        return {
            "question": question,
            "answer": result.get("answer"),
            "sources": result.get("sources", []),
        }