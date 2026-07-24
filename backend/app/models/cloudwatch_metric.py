from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from sqlalchemy import Float
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.lambda_function import LambdaFunction


class CloudWatchMetric(Base):
    __tablename__ = "cloudwatch_metrics"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lambda_id: Mapped[int] = mapped_column(
        ForeignKey("lambda_functions.id"),
        index=True,
        nullable=False
    )

    metric_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    metric_value: Mapped[float] = mapped_column(Float)

    unit: Mapped[str] = mapped_column(
        String(50)
    )

    metric_timestamp: Mapped[datetime] = mapped_column(
        DateTime
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    lambda_function: Mapped["LambdaFunction"] = relationship(
    "LambdaFunction",
    back_populates="metrics"
)