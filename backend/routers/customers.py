from fastapi import APIRouter, Depends

from backend.schemas.customer import CustomerRead
from backend.schemas.order import OrderRead
from backend.services.customer_service import CustomerService, get_customer_service
from backend.services.order_service import OrderService, get_order_service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.get_by_id(customer_id)


@router.get("/{customer_id}/orders", response_model=list[OrderRead])
async def get_customer_orders(
    customer_id: int,
    service: OrderService = Depends(get_order_service),
):
    return await service.get_customer_orders(customer_id)
