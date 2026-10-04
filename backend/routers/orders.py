from fastapi import APIRouter, Depends

from backend.schemas.order import OrderRead
from backend.services.order_service import OrderService, get_order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
async def list_orders(service: OrderService = Depends(get_order_service)):
    return await service.list_all()


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    return await service.get_by_id(order_id)
