from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class RagQueryRequest(BaseModel):
    query: str


class RagContextItem(BaseModel):
    source: str
    item: str


class RagQueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_context: List[RagContextItem]
    confidence_score: str


class RagReindexResponse(BaseModel):
    status: str
    total_chunks_indexed: int
