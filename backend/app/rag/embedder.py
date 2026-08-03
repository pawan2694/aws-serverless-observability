"""
RAG Embedder & Vector Similarity Engine.

Yeh module text ko numerical vectors mein convert karta hai.
Current implementation simple bag-of-words approach use karta hai, matlab har word ki frequency
count karke ek normalized vector banaya jata hai.

Cosine similarity ka use karke hum check karte hain ki query aur chunk kitne similar hain.
"""

import math
import re
from typing import List, Dict, Any


class TextEmbedder:
    """
    Text ko vector representation mein convert karta hai.

    Is implementation mein vocabulary build ki jati hai aur phir har text ko
    us vocabulary ke hisaab se numeric vector mein map kiya jata hai.
    """

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        """Text ko lowercase alphanumeric tokens mein tod deta hai."""
        return re.findall(r'\w+', text.lower())

    def build_vocabulary(self, corpus: List[str]):
        """Har chunk ke words se vocabulary build karta hai."""
        self.vocabulary = {}
        for doc in corpus:
            tokens = self._tokenize(doc)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)

    def embed_text(self, text: str) -> List[float]:
        """Ek text ko normalized vector mein convert karta hai."""
        tokens = self._tokenize(text)
        vector = [0.0] * max(len(self.vocabulary), 1)

        if not self.vocabulary:
            return vector

        # Har token ka count vector mein daala jata hai.
        for token in tokens:
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                vector[idx] += 1.0

        # L2 normalization se vector ko consistent banaya jata hai.
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Do vectors ke beech cosine similarity calculate karta hai.

        1.0 ka matlab bilkul same/strong match,
        0.0 ka matlab unrelated.
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        return float(dot_product)
