from decimal import Decimal

import pytest
import pytest_asyncio

from backend.models.category import Category
from backend.models.product import Product
from backend.repositories.category_repository import CategoryRepository
from backend.repositories.product_repository import ProductRepository
from backend.services.product_service import ProductService


@pytest_asyncio.fixture
async def seeded_products(db_session) -> list[Product]:
    notebooks = Category(name="Notebooks")
    db_session.add(notebooks)
    await db_session.flush()

    products = [
        Product(
            name="Lenovo ThinkPad",
            description="notebook corporativo",
            brand="Lenovo",
            category_id=notebooks.id,
            price=Decimal("900.00"),
            stock=5,
        ),
        Product(
            name="Dell Inspiron",
            description="notebook para uso geral",
            brand="Dell",
            category_id=notebooks.id,
            price=Decimal("1200.00"),
            stock=3,
        ),
    ]
    db_session.add_all(products)
    await db_session.flush()
    return products


def _service(db_session) -> ProductService:
    return ProductService(ProductRepository(db_session), CategoryRepository(db_session))


@pytest.mark.asyncio
async def test_search_is_case_insensitive(db_session, seeded_products):
    results = await _service(db_session).search(search="LENOVO")

    assert [p.name for p in results] == ["Lenovo ThinkPad"]


@pytest.mark.asyncio
async def test_search_respects_max_price_boundary(db_session, seeded_products):
    results = await _service(db_session).search(max_price=Decimal("900.00"))

    assert [p.name for p in results] == ["Lenovo ThinkPad"]


@pytest.mark.asyncio
async def test_search_matches_description(db_session, seeded_products):
    results = await _service(db_session).search(search="uso geral")

    assert [p.name for p in results] == ["Dell Inspiron"]


@pytest.mark.asyncio
async def test_search_unknown_category_returns_empty_list(db_session, seeded_products):
    results = await _service(db_session).search(category="CategoriaFake")

    assert results == []
