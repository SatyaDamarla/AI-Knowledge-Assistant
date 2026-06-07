from typing import List

from models.source_models import ChunkRecord, LoadedSourceContent

from src.ingestion.text_loader import TextLoader
from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.youtube_loader import YouTubeLoader

from src.ingestion.chunkers.recursive_chunker import RecursiveChunker
from src.ingestion.embedders.gemini_embedder import GeminiEmbedder
from src.ingestion.indexers.faiss_indexer import FaissIndexer


class IngestionPipeline:
    """
    End-to-end pipeline:
    loader → chunker → embedder → indexer
    """

    def __init__(self):
        self.chunker = RecursiveChunker()
        self.embedder = GeminiEmbedder()
        

    def run(self, source) -> List[ChunkRecord]:
        """
        Takes SourceRecord → indexes it
        """

        content = self._load_source(source)

        chunks = self.chunker.chunk(content)

        if not chunks:
            return []

        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_batch(texts)

        embedding_dim = len(embeddings[0])

        indexer = FaissIndexer(
            embedding_dim=embedding_dim,
            user_id=source.user_id,
        )

        indexer.add(chunks, embeddings)
        indexer.save()

        return chunks

    def _load_source(self, source) -> LoadedSourceContent:
        """
        Select correct loader based on source_type
        and attach user_id into loaded content metadata.
        """

        if source.source_type == "text":
            loader = TextLoader(
                source_id=source.source_id,
                title=source.title,
                file_path=source.raw_text_path,
            )

        elif source.source_type == "pdf":
            loader = PDFLoader(
                source_id=source.source_id,
                title=source.title,
                file_path=source.storage_path,
            )

        elif source.source_type == "youtube":
            loader = YouTubeLoader(
                source_id=source.source_id,
                title=source.title,
                url=source.url,
            )

        else:
            raise ValueError(f"Unsupported source type: {source.source_type}")

        content = loader.load()

        content.user_id = source.user_id
        content.metadata["user_id"] = source.user_id

        return content