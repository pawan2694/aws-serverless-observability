from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LambdaFunction(Base):
    __tablename__ = "lambda_functions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    function_name: Mapped[str] = mapped_column(
        String(255),
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

    memory_size: Mapped[int] = mapped_column(
        Integer
    )

    timeout: Mapped[int] = mapped_column(
        Integer
    )

    last_modified: Mapped[str] = mapped_column(
        String(100)
    )

    code_size: Mapped[int] = mapped_column(
        Integer
    )

    architecture: Mapped[str] = mapped_column(
        String(50)
    )