"""
RAG Embedder & Vector Similarity Engine

Converts text strings into high-dimensional numerical vector representations.
Implements Cosine Similarity math to measure semantic closeness between user queries
and database chunks.

Math Formula for Cosine Similarity:
CosineSimilarity(A, B) = (A dot B) / (||A|| * ||B||)
"""

import math
import re
from typing import List, Dict, Any


class TextEmbedder:
    """
    Computes vector embeddings and similarity scores for text strings.
    Uses word-level frequency vectorization with normalization to generate dense vectors.
    """

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenizes text into lowercase alphanumeric words.
        """
        return re.findall(r'\w+', text.lower())

    def build_vocabulary(self, corpus: List[str]):
        """
        Builds a vocabulary mapping for all words in the document chunks corpus.
        """
        self.vocabulary = {}
        for doc in corpus:
            tokens = self._tokenize(doc)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)

    def embed_text(self, text: str) -> List[float]:
        """
        Converts a text string into a normalized numerical vector representation.
        """
        tokens = self._tokenize(text)
        vector = [0.0] * max(len(self.vocabulary), 1)

        if not self.vocabulary:
            return vector

        for token in tokens:
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                vector[idx] += 1.0

        # L2 Vector Normalization
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculates the Cosine Similarity metric between two normalized vector embeddings.
        Returns a score between 0.0 (unrelated) and 1.0 (identical/highest similarity).
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        return float(dot_product)
