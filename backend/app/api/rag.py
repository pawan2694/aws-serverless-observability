from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.rag import RagQueryRequest, RagQueryResponse, RagReindexResponse
from app.services.rag_service import RagService

router = APIRouter(
    prefix="/rag",
    tags=["RAG Engine"]
)


@router.post(
    "/query",
    response_model=RagQueryResponse,
    summary="Process RAG Question & Vector Context Retrieval"
)
def query_rag(
    payload: RagQueryRequest,
    db: Session = Depends(get_db)
):
    """User query ko le kar full RAG pipeline run karta hai."""
    service = RagService(db)
    return service.process_query(payload.query)


@router.post(
    "/reindex",
    response_model=RagReindexResponse,
    summary="Rebuild RAG Vector Store Index"
)
def reindex_rag(
    db: Session = Depends(get_db)
):
    """DB se fresh data lekar vector index ko rebuild karta hai."""
    service = RagService(db)
    total = service.reindex()
    return {
        "status": "success",
        "total_chunks_indexed": total
    }
