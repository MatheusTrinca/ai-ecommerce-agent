from datetime import UTC, datetime, timedelta

import pytest

from backend.models.customer import Customer
from backend.models.order import Order, OrderStatus
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.order_repository import OrderRepository
from backend.services.exceptions import NotFoundError
from backend.services.order_service import OrderService


def _service(db_session) -> OrderService:
    return OrderService(OrderRepository(db_session), CustomerRepository(db_session))


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

    orders = await _service(db_session).get_customer_orders(joao.id)

    assert len(orders) == 1
    assert orders[0].customer_id == joao.id


@pytest.mark.asyncio
async def test_get_customer_orders_raises_when_customer_missing(db_session):
    with pytest.raises(NotFoundError):
        await _service(db_session).get_customer_orders(999)


@pytest.mark.asyncio
async def test_get_by_id_raises_when_order_missing(db_session):
    with pytest.raises(NotFoundError):
        await _service(db_session).get_by_id(999)


@pytest.mark.asyncio
async def test_search_filters_by_status(db_session):
    joao = Customer(name="João", email="joao@example.com")
    db_session.add(joao)
    await db_session.flush()

    db_session.add_all(
        [
            Order(customer_id=joao.id, status=OrderStatus.PENDING),
            Order(customer_id=joao.id, status=OrderStatus.DELIVERED),
        ]
    )
    await db_session.flush()

    results = await _service(db_session).search(status=OrderStatus.DELIVERED)

    assert [o.status for o in results] == [OrderStatus.DELIVERED]


@pytest.mark.asyncio
async def test_search_unknown_customer_returns_empty_list(db_session):
    results = await _service(db_session).search(customer_id=999)

    assert results == []


@pytest.mark.asyncio
async def test_get_customer_orders_respects_date_range(db_session):
    joao = Customer(name="João", email="joao@example.com")
    db_session.add(joao)
    await db_session.flush()

    now = datetime.now(UTC)
    old_order = Order(customer_id=joao.id, status=OrderStatus.DELIVERED, created_at=now - timedelta(days=60))
    recent_order = Order(customer_id=joao.id, status=OrderStatus.DELIVERED, created_at=now - timedelta(days=1))
    db_session.add_all([old_order, recent_order])
    await db_session.flush()

    results = await _service(db_session).get_customer_orders(
        joao.id, date_from=now - timedelta(days=5)
    )

    assert [o.id for o in results] == [recent_order.id]


@pytest.mark.asyncio
async def test_check_status_is_late_when_overdue_and_not_finished(db_session):
    joao = Customer(name="João", email="joao@example.com")
    db_session.add(joao)
    await db_session.flush()

    order = Order(
        customer_id=joao.id,
        status=OrderStatus.SHIPPED,
        estimated_delivery=datetime.now(UTC) - timedelta(days=3),
    )
    db_session.add(order)
    await db_session.flush()

    result = await _service(db_session).check_status(order.id)

    assert result.is_late is True


@pytest.mark.asyncio
async def test_check_status_is_not_late_when_delivered(db_session):
    joao = Customer(name="João", email="joao@example.com")
    db_session.add(joao)
    await db_session.flush()

    order = Order(
        customer_id=joao.id,
        status=OrderStatus.DELIVERED,
        estimated_delivery=datetime.now(UTC) - timedelta(days=3),
    )
    db_session.add(order)
    await db_session.flush()

    result = await _service(db_session).check_status(order.id)

    assert result.is_late is False


@pytest.mark.asyncio
async def test_check_status_is_not_late_without_estimated_delivery(db_session):
    joao = Customer(name="João", email="joao@example.com")
    db_session.add(joao)
    await db_session.flush()

    order = Order(customer_id=joao.id, status=OrderStatus.PENDING)
    db_session.add(order)
    await db_session.flush()

    result = await _service(db_session).check_status(order.id)

    assert result.is_late is False


@pytest.mark.asyncio
async def test_check_status_raises_when_order_missing(db_session):
    with pytest.raises(NotFoundError):
        await _service(db_session).check_status(999)
