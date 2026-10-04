from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.order import Order
from backend.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _select_with_items(self) -> Select[tuple[Order]]:
        return select(Order).options(selectinload(Order.items).selectinload(OrderItem.product))

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self._session.execute(self._select_with_items().where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Order]:
        result = await self._session.execute(self._select_with_items())
        return list(result.scalars().all())

    async def list_by_customer_id(self, customer_id: int) -> list[Order]:
        result = await self._session.execute(
            self._select_with_items().where(Order.customer_id == customer_id)
        )
        return list(result.scalars().all())
