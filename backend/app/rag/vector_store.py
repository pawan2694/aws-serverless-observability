"""
RAG Vector Store Engine.

Yeh module in-memory vector index maintain karta hai.
Chunk embeddings ko store karke query ke liye similarity search karta hai.
"""

from typing import List, Dict, Any
from app.rag.embedder import TextEmbedder


class VectorStore:
    """
    In-memory vector database index.

    Current implementation simple aur lightweight hai.
    Production mein isko FAISS, pgvector ya Elasticsearch jaise tools se replace kiya ja sakta hai.
    """

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []
        self.embedder = TextEmbedder()
        self.is_indexed = False

    def build_index(self, chunks: List[Dict[str, Any]]):
        """
        Chunks ko index karta hai.

        1. Sabhi chunks ka corpus build hota hai.
        2. Vocabulary ban ke vector embeddings generate hoti hain.
        3. Index mark ho jata hai.
        """
        self.chunks = chunks
        corpus = [chunk["text"] for chunk in chunks]

        # Vocabulary build karna zaroori hai taaki har chunk ka vector consistent bane.
        self.embedder.build_vocabulary(corpus)

        # Har chunk ke liye vector embedding generate karna.
        self.embeddings = [self.embedder.embed_text(text) for text in corpus]
        self.is_indexed = True
        print(f"✅ VectorStore Index built with {len(self.chunks)} text chunks.")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query ke liye top-k most similar chunks return karta hai.

        Process:
        1. Query ko vector mein convert karna
        2. Har chunk se cosine similarity calculate karna
        3. Highest score wale top-k chunna
        """
        if not self.is_indexed or not self.chunks:
            return []

        query_vector = self.embedder.embed_text(query)

        results = []
        for chunk, chunk_vector in zip(self.chunks, self.embeddings):
            score = self.embedder.cosine_similarity(query_vector, chunk_vector)
            results.append({
                "chunk": chunk,
                "score": score
            })

        # Highest similarity score ke hisaab se sort karna.
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]
