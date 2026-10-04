from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.category import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1000))
    brand: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    specs: Mapped[dict] = mapped_column(JSON, default=dict)
    stock: Mapped[int] = mapped_column(default=0)

    category: Mapped["Category"] = relationship()
