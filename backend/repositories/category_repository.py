from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.category import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Category | None:
        result = await self._session.execute(select(Category).where(Category.name.ilike(name)))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(select(Category))
        return list(result.scalars().all())
