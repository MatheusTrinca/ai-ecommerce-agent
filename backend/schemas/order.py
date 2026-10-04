from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.models.order import OrderStatus
from backend.schemas.order_item import OrderItemRead


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    status: OrderStatus
    created_at: datetime
    shipped_at: datetime | None
    estimated_delivery: datetime | None
    items: list[OrderItemRead]
