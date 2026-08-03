"""
RAG Vector Store Engine

Maintains the vector index of chunk embeddings in memory.
Performs Top-K similarity searches against the user's query vector.
"""

from typing import List, Dict, Any
from app.rag.embedder import TextEmbedder


class VectorStore:
    """
    In-memory Vector Database Index.
    Stores chunks along with their computed vector embeddings.
    """

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []
        self.embedder = TextEmbedder()
        self.is_indexed = False

    def build_index(self, chunks: List[Dict[str, Any]]):
        """
        Indexes the given list of text chunks:
        1. Builds vocabulary across all chunk texts.
        2. Computes vector embeddings for each chunk.
        """
        self.chunks = chunks
        corpus = [chunk["text"] for chunk in chunks]

        # Build vocabulary matrix
        self.embedder.build_vocabulary(corpus)

        # Generate vector embeddings
        self.embeddings = [self.embedder.embed_text(text) for text in corpus]
        self.is_indexed = True
        print(f"✅ VectorStore Index built with {len(self.chunks)} text chunks.")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes Vector Search:
        1. Embeds the user query into a vector representation.
        2. Calculates Cosine Similarity score against every chunk vector.
        3. Returns top-K highest scoring chunks.
        """
        if not self.is_indexed or not self.chunks:
            return []

        query_vector = self.embedder.embed_text(query)

        results = []
        for idx, (chunk, chunk_vector) in enumerate(zip(self.chunks, self.embeddings)):
            score = self.embedder.cosine_similarity(query_vector, chunk_vector)
            results.append({
                "chunk": chunk,
                "score": score
            })

        # Sort descending by similarity score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Return top-K matches
        return results[:top_k]
