from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from backend.schemas.product import ProductRead


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: ProductRead
