"""
RAG Coordinator Service

Integrates chunker, vector store, and generator into a single unified service.
Manages global vector index state across application requests.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session

from app.rag.chunker import TelemetryChunker
from app.rag.vector_store import VectorStore
from app.rag.generator import RagGenerator

# Global Singleton VectorStore instance
_global_vector_store = VectorStore()


class RagService:

    def __init__(self, db: Session):
        self.db = db
        self.vector_store = _global_vector_store
        self.generator = RagGenerator()

    def ensure_indexed(self):
        """
        Ensures the vector store index is populated from PostgreSQL DB.
        """
        if not self.vector_store.is_indexed:
            self.reindex()

    def reindex(self) -> int:
        """
        Re-chunks database logs/metrics and rebuilds the vector store index.
        """
        chunker = TelemetryChunker(self.db)
        chunks = chunker.create_chunks()
        self.vector_store.build_index(chunks)
        return len(chunks)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Full RAG Pipeline Execution:
        1. Ensures database telemetry is indexed in vector store.
        2. Vector Similarity Search (Top-K=3 matching chunks).
        3. Prompt Augmentation & Response Generation.
        """
        self.ensure_indexed()

        # Step 1 & 2: Embed Query & Vector Search
        search_results = self.vector_store.search(query, top_k=3)

        # Step 3: Augment Prompt & Generate Response
        result = self.generator.generate_response(query, search_results)
        return result
