from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.models.order import Order
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.order_repository import OrderRepository
from backend.services.exceptions import NotFoundError


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        customer_repository: CustomerRepository,
    ) -> None:
        self._order_repository = order_repository
        self._customer_repository = customer_repository

    async def get_by_id(self, order_id: int) -> Order:
        order = await self._order_repository.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"Order {order_id} not found")
        return order

    async def list_all(self) -> list[Order]:
        return await self._order_repository.list_all()

    async def get_customer_orders(self, customer_id: int) -> list[Order]:
        customer = await self._customer_repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")
        return await self._order_repository.list_by_customer_id(customer_id)


def get_order_service(session: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(session), CustomerRepository(session))
