from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, customer_id: int) -> Customer | None:
        result = await self._session.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()

    async def search(self, name: str | None = None, email: str | None = None) -> list[Customer]:
        """Busca clientes por nome e/ou email, case-insensitive, combináveis com AND.

        Qualquer filtro None não restringe o resultado. Sem filtros, devolve todos.
        """
        stmt = select(Customer)

        clauses = []
        if name is not None:
            clauses.append(Customer.name.ilike(f"%{name}%"))
        if email is not None:
            clauses.append(Customer.email.ilike(f"%{email}%"))

        if clauses:
            stmt = stmt.where(and_(*clauses))

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
