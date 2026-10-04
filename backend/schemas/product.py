from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    brand: str
    category_id: int
    price: Decimal
    specs: dict
    stock: int
