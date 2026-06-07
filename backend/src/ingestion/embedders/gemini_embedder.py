import os
from typing import List

from dotenv import load_dotenv
import google.generativeai as genai

from src.ingestion.embedders.base_embedder import BaseEmbedder


class GeminiEmbedder(BaseEmbedder):
    """
    Gemini embedding wrapper.
    """

    def __init__(self, model_name: str = "models/gemini-embedding-001"):
        load_dotenv()

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY is missing from .env")

        genai.configure(api_key=api_key)
        self.model_name = model_name

    def embed_text(self, text: str) -> List[float]:
        response = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document",
        )

        return response["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []

        for text in texts:
            embeddings.append(self.embed_text(text))

        return embeddings