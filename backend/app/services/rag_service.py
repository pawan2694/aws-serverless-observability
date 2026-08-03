"""
RAG Coordinator Service.

Yeh service chunker, vector store aur generator ko ek saath jod kar
complete RAG pipeline ka coordinator ka kaam karta hai.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session

from app.rag.chunker import TelemetryChunker
from app.rag.vector_store import VectorStore
from app.rag.generator import RagGenerator

# Global singleton vector store: har request ke liye same index reuse ho.
_global_vector_store = VectorStore()


class RagService:

    def __init__(self, db: Session):
        self.db = db
        self.vector_store = _global_vector_store
        self.generator = RagGenerator()

    def ensure_indexed(self):
        """
        Ensure karta hai ki vector index already build ho chuka ho.

        Agar index abhi nahi hai to reindex kar diya jata hai.
        """
        if not self.vector_store.is_indexed:
            self.reindex()

    def reindex(self) -> int:
        """
        DB se fresh data lekar chunks banata hai aur vector store ko rebuild karta hai.

        Isko /rag/reindex endpoint ke through call kiya jata hai jab DB mein new data aaye.
        """
        chunker = TelemetryChunker(self.db)
        chunks = chunker.create_chunks()
        self.vector_store.build_index(chunks)
        return len(chunks)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Full RAG pipeline execute karta hai.

        1. Ensure index exists
        2. Query ko vector search se match karna
        3. Retrieved context ko generator ke saath combine karna
        """
        self.ensure_indexed()

        # Step 1: Query ko vector search ke liye bhejna.
        search_results = self.vector_store.search(query, top_k=3)

        # Step 2: Retrieved context ke basis par answer generate karna.
        result = self.generator.generate_response(query, search_results)
        return result
