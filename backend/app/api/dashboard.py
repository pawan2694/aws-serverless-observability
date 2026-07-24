from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.dashboard import DashboardSummary, HighDurationResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.get_summary()

@router.get(
    "/high-duration",
    response_model=list[HighDurationResponse],
)
def high_duration(
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.get_high_duration()