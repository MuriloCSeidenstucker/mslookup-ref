# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods, E1102:not-callable

from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.settings.base import Base


class DrugEntity(Base):

    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    registration_number: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    product_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    active_ingredient: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    regulatory_category: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    registration_holder: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    registration_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    registration_expiration_date: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
    )

    product_name_normalized: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    active_ingredient_normalized: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    registration_holder_normalized: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    regulatory_category_normalized: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    is_registration_valid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


Index("ix_drugs_registration_number", DrugEntity.registration_number)
Index("ix_drugs_product_name_normalized", DrugEntity.product_name_normalized)
Index("ix_drugs_active_ingredient_normalized", DrugEntity.active_ingredient_normalized)
Index(
    "ix_drugs_registration_holder_normalized", DrugEntity.registration_holder_normalized
)
Index(
    "ix_drugs_regulatory_category_normalized", DrugEntity.regulatory_category_normalized
)
Index("ix_drugs_is_registration_valid", DrugEntity.is_registration_valid)
