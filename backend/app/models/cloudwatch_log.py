from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.lambda_function import LambdaFunction


class CloudWatchLog(Base):
    __tablename__ = "cloudwatch_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lambda_id: Mapped[int] = mapped_column(
        ForeignKey("lambda_functions.id"),
        index=True,
        nullable=False

    )

    request_id: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    event_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    log_stream_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    log_timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    ingestion_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    lambda_function: Mapped["LambdaFunction"] = relationship(
        "LambdaFunction",
        back_populates="logs"
    )