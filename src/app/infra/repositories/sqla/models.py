from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import func, Index
from sqlalchemy.orm import (
    declarative_mixin,
    mapped_column,
    Mapped
)

from app.domain.carts.value_objects import CartStatusEnum
from app.infra.repositories.sqla.base import Base


@declarative_mixin
class TimestampMixin:
    timestamp = Annotated[
        datetime,
        mapped_column(
            nullable=False,
            default=datetime.utcnow,
            server_default=func.CURRENT_TIMESTAMP(),
        ),
    ]

    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp] = mapped_column(
        onupdate=datetime.utcnow,
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )


class Cart(TimestampMixin, Base):
    __tablename__ = "carts"

    id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    status: Mapped[CartStatusEnum] = mapped_column(
        default=CartStatusEnum.OPENED,
        server_default=CartStatusEnum.OPENED.value,
    )

    __table_args__ = (
        Index(
            "idx_user_id_opened_status_unique",
            "user_id",
            "status",
            unique=True,
            postgresql_where=(
                status.in_([CartStatusEnum.OPENED.value, CartStatusEnum.LOCKED.value])
            ),
        ),
    )
