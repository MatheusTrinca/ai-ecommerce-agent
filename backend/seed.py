import asyncio
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import text

from backend.db.session import AsyncSessionLocal
from backend.models.category import Category
from backend.models.customer import Customer
from backend.models.order import Order, OrderStatus
from backend.models.order_item import OrderItem
from backend.models.product import Product


async def seed(session) -> None:
    await session.execute(
        text(
            "TRUNCATE TABLE order_items, orders, products, categories, customers "
            "RESTART IDENTITY CASCADE"
        )
    )

    now = datetime.now(UTC)

    notebooks = Category(name="Notebooks")
    acessorios = Category(name="Acessórios")
    session.add_all([notebooks, acessorios])
    await session.flush()

    joao = Customer(name="João", email="joao@example.com")
    matheus = Customer(name="Matheus", email="matheus@example.com")
    session.add_all([joao, matheus])
    await session.flush()

    thinkpad = Product(
        name="Lenovo ThinkPad E14",
        description="Notebook corporativo 14'' com SSD",
        brand="Lenovo",
        category_id=notebooks.id,
        price=Decimal("899.90"),
        specs={"ram_gb": 8, "storage_gb": 256},
        stock=10,
    )
    legion = Product(
        name="Lenovo Legion 5",
        description="Notebook gamer com placa de vídeo dedicada",
        brand="Lenovo",
        category_id=notebooks.id,
        price=Decimal("1499.90"),
        specs={"ram_gb": 16, "storage_gb": 512},
        stock=0,
    )
    dell = Product(
        name="Dell Inspiron 15",
        description="Notebook para uso geral",
        brand="Dell",
        category_id=notebooks.id,
        price=Decimal("1099.00"),
        specs={"ram_gb": 8, "storage_gb": 256},
        stock=7,
    )
    mouse = Product(
        name="Logitech MX Master 3",
        description="Mouse sem fio de alta precisão",
        brand="Logitech",
        category_id=acessorios.id,
        price=Decimal("349.90"),
        specs={},
        stock=20,
    )
    session.add_all([thinkpad, legion, dell, mouse])
    await session.flush()

    order_12345 = Order(
        id=12345,
        customer_id=joao.id,
        status=OrderStatus.SHIPPED,
        created_at=now - timedelta(days=10),
        shipped_at=now - timedelta(days=8),
        estimated_delivery=now - timedelta(days=3),
    )
    order_joao_recent = Order(
        customer_id=joao.id,
        status=OrderStatus.DELIVERED,
        created_at=now - timedelta(days=2),
        shipped_at=now - timedelta(days=1),
        estimated_delivery=now - timedelta(hours=12),
    )
    order_matheus_pending = Order(
        customer_id=matheus.id,
        status=OrderStatus.PENDING,
    )
    session.add_all([order_12345, order_joao_recent, order_matheus_pending])
    await session.flush()

    session.add_all(
        [
            OrderItem(
                order_id=order_12345.id,
                product_id=thinkpad.id,
                quantity=1,
                unit_price=thinkpad.price,
            ),
            OrderItem(
                order_id=order_joao_recent.id,
                product_id=mouse.id,
                quantity=2,
                unit_price=mouse.price,
            ),
            OrderItem(
                order_id=order_matheus_pending.id,
                product_id=dell.id,
                quantity=1,
                unit_price=dell.price,
            ),
        ]
    )
    await session.flush()

    # order_12345 tem id explícito (fora da sequence); sincroniza orders_id_seq
    # para não colidir com o próximo pedido criado sem id explícito.
    await session.execute(text("SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders))"))


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await seed(session)
    print("Seed concluído.")


if __name__ == "__main__":
    asyncio.run(main())
