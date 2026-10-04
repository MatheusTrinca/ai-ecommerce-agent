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
