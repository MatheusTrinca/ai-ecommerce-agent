from datetime import datetime

from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.order import Order, OrderStatus
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

    async def search(
        self,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Order]:
        """Busca pedidos com filtros opcionais e combináveis entre si (AND).

        - status: pedido deve estar exatamente nesse status.
        - customer_id: pedido deve pertencer a esse cliente.
        - date_from/date_to: created_at deve estar dentro do intervalo (ambos inclusivos).
        """
        stmt = self._select_with_items()

        clauses = []
        if status is not None:
            clauses.append(Order.status == status)
        if customer_id is not None:
            clauses.append(Order.customer_id == customer_id)
        if date_from is not None:
            clauses.append(Order.created_at >= date_from)
        if date_to is not None:
            clauses.append(Order.created_at <= date_to)

        if clauses:
            stmt = stmt.where(and_(*clauses))

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
