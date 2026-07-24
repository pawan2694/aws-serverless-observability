from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ai_recommendation import AIRecommendation
    from app.models.cloudwatch_log import CloudWatchLog
    from app.models.cloudwatch_metric import CloudWatchMetric


class LambdaFunction(Base):
    __tablename__ = "lambda_functions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    function_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    function_arn: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False
    )

    runtime: Mapped[str] = mapped_column(
        String(100)
    )

    handler: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[str] = mapped_column(
        String(500)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    timeout: Mapped[int] = mapped_column(
        Integer
    )

    memory_size: Mapped[int] = mapped_column(
        Integer
    )

    code_size: Mapped[int] = mapped_column(
        Integer
    )

    version: Mapped[str] = mapped_column(
        String(50)
    )

    package_type: Mapped[str] = mapped_column(
        String(50)
    )

    architecture: Mapped[str] = mapped_column(
        String(100)
    )

    last_modified: Mapped[str] = mapped_column(
        String(100)
    )

    log_group: Mapped[str] = mapped_column(
        String(500)
    )

    revision_id: Mapped[str] = mapped_column(
        String(100)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    metrics: Mapped[list["CloudWatchMetric"]] = relationship(
        "CloudWatchMetric",
        back_populates="lambda_function",
        cascade="all, delete-orphan",
    )

    logs: Mapped[list["CloudWatchLog"]] = relationship(
        "CloudWatchLog",
        back_populates="lambda_function",
        cascade="all, delete-orphan",
    )

    recommendations: Mapped[list["AIRecommendation"]] = relationship(
        "AIRecommendation",
        back_populates="lambda_function",
        cascade="all, delete-orphan",
    )