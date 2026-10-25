from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self._category_repository = category_repository

    async def list_all(self) -> list[Category]:
        return await self._category_repository.list_all()


def get_category_service(session: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(session))
