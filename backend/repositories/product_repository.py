from decimal import Decimal

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def search(
        self,
        search: str | None = None,
        category_id: int | None = None,
        max_price: Decimal | None = None,
    ) -> list[Product]:
        """Busca produtos com filtros opcionais e combináveis entre si (AND).

        - search: substring case-insensitive encontrada em name OU description OU brand.
        - category_id: produto deve pertencer exatamente a essa categoria.
        - max_price: price deve ser <= max_price (limite superior inclusivo).

        Qualquer filtro que seja None não deve restringir o resultado (comporta-se
        como "sem filtro nesse campo"). Se todos forem None, devolve todos os produtos.
        """
        stmt = select(Product)

        clauses = []
        if search is not None:
            term = f"%{search}%"
            clauses.append(
                or_(
                    Product.name.ilike(term),
                    Product.description.ilike(term),
                    Product.brand.ilike(term),
                )
            )
        if category_id is not None:
            clauses.append(Product.category_id == category_id)
        if max_price is not None:
            clauses.append(Product.price <= max_price)

        if clauses:
            stmt = stmt.where(and_(*clauses))

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
