from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, customer_id: int) -> Customer | None:
        result = await self._session.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()
