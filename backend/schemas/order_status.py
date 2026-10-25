from datetime import datetime

from pydantic import BaseModel

from backend.models.order import OrderStatus


class OrderStatusRead(BaseModel):
    order_id: int
    status: OrderStatus
    is_late: bool
    estimated_delivery: datetime | None
