from datetime import UTC, datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.models.order import Order, OrderStatus
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.order_repository import OrderRepository
from backend.schemas.order_status import OrderStatusRead
from backend.services.exceptions import NotFoundError

_FINISHED_STATUSES = (OrderStatus.DELIVERED, OrderStatus.CANCELLED)


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

    async def search(
        self,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Order]:
        return await self._order_repository.search(
            status=status, customer_id=customer_id, date_from=date_from, date_to=date_to
        )

    async def get_customer_orders(
        self,
        customer_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Order]:
        customer = await self._customer_repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")
        return await self._order_repository.search(
            customer_id=customer_id, date_from=date_from, date_to=date_to
        )

    async def check_status(self, order_id: int) -> OrderStatusRead:
        order = await self.get_by_id(order_id)

        is_late = (
            order.estimated_delivery is not None
            and order.estimated_delivery < datetime.now(UTC)
            and order.status not in _FINISHED_STATUSES
        )

        return OrderStatusRead(
            order_id=order.id,
            status=order.status,
            is_late=is_late,
            estimated_delivery=order.estimated_delivery,
        )


def get_order_service(session: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(session), CustomerRepository(session))
