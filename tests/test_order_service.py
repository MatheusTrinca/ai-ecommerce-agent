import pytest

from backend.models.customer import Customer
from backend.models.order import Order, OrderStatus
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.order_repository import OrderRepository
from backend.services.exceptions import NotFoundError
from backend.services.order_service import OrderService


@pytest.mark.asyncio
async def test_get_customer_orders_returns_only_that_customer_orders(db_session):
    joao = Customer(name="João", email="joao@example.com")
    matheus = Customer(name="Matheus", email="matheus@example.com")
    db_session.add_all([joao, matheus])
    await db_session.flush()

    db_session.add_all(
        [
            Order(customer_id=joao.id, status=OrderStatus.PENDING),
            Order(customer_id=matheus.id, status=OrderStatus.PENDING),
        ]
    )
    await db_session.flush()

    service = OrderService(OrderRepository(db_session), CustomerRepository(db_session))
    orders = await service.get_customer_orders(joao.id)

    assert len(orders) == 1
    assert orders[0].customer_id == joao.id


@pytest.mark.asyncio
async def test_get_customer_orders_raises_when_customer_missing(db_session):
    service = OrderService(OrderRepository(db_session), CustomerRepository(db_session))

    with pytest.raises(NotFoundError):
        await service.get_customer_orders(999)


@pytest.mark.asyncio
async def test_get_by_id_raises_when_order_missing(db_session):
    service = OrderService(OrderRepository(db_session), CustomerRepository(db_session))

    with pytest.raises(NotFoundError):
        await service.get_by_id(999)
