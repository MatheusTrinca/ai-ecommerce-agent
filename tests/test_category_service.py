import pytest

from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository
from backend.services.category_service import CategoryService


@pytest.mark.asyncio
async def test_list_all_returns_every_category(db_session):
    db_session.add_all([Category(name="Notebooks"), Category(name="Acessórios")])
    await db_session.flush()

    service = CategoryService(CategoryRepository(db_session))
    results = await service.list_all()

    assert sorted(c.name for c in results) == ["Acessórios", "Notebooks"]


@pytest.mark.asyncio
async def test_list_all_returns_empty_list_when_no_categories(db_session):
    service = CategoryService(CategoryRepository(db_session))

    results = await service.list_all()

    assert results == []
