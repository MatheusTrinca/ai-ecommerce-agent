import pytest

from backend.models.customer import Customer
from backend.repositories.customer_repository import CustomerRepository
from backend.services.customer_service import CustomerService
from backend.services.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_get_by_id_returns_existing_customer(db_session):
    customer = Customer(name="Ana", email="ana@example.com")
    db_session.add(customer)
    await db_session.flush()

    service = CustomerService(CustomerRepository(db_session))
    result = await service.get_by_id(customer.id)

    assert result.name == "Ana"


@pytest.mark.asyncio
async def test_get_by_id_raises_not_found_when_missing(db_session):
    service = CustomerService(CustomerRepository(db_session))

    with pytest.raises(NotFoundError):
        await service.get_by_id(999)


@pytest.mark.asyncio
async def test_search_by_name_is_case_insensitive_and_partial(db_session):
    db_session.add_all(
        [
            Customer(name="João Silva", email="joao@example.com"),
            Customer(name="Matheus", email="matheus@example.com"),
        ]
    )
    await db_session.flush()

    service = CustomerService(CustomerRepository(db_session))
    results = await service.search(name="joão")

    assert [c.name for c in results] == ["João Silva"]


@pytest.mark.asyncio
async def test_search_by_email(db_session):
    db_session.add_all(
        [
            Customer(name="João Silva", email="joao@example.com"),
            Customer(name="Matheus", email="matheus@example.com"),
        ]
    )
    await db_session.flush()

    service = CustomerService(CustomerRepository(db_session))
    results = await service.search(email="matheus@")

    assert [c.name for c in results] == ["Matheus"]


@pytest.mark.asyncio
async def test_search_with_no_filters_returns_all(db_session):
    db_session.add_all(
        [
            Customer(name="João Silva", email="joao@example.com"),
            Customer(name="Matheus", email="matheus@example.com"),
        ]
    )
    await db_session.flush()

    service = CustomerService(CustomerRepository(db_session))
    results = await service.search()

    assert len(results) == 2


@pytest.mark.asyncio
async def test_search_no_match_returns_empty_list(db_session):
    service = CustomerService(CustomerRepository(db_session))

    results = await service.search(name="Alguém Que Não Existe")

    assert results == []
