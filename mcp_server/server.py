from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from backend.db.session import AsyncSessionLocal
from backend.models.order import OrderStatus
from backend.schemas.category import CategoryRead
from backend.schemas.customer import CustomerRead
from backend.schemas.order import OrderRead
from backend.schemas.order_status import OrderStatusRead
from backend.schemas.product import ProductRead
from backend.services.category_service import get_category_service
from backend.services.customer_service import get_customer_service
from backend.services.exceptions import NotFoundError
from backend.services.order_service import get_order_service
from backend.services.product_service import get_product_service

mcp = MCPServer("ai-commerce-agent")


@contextmanager
def _as_tool_error():
    """Traduz NotFoundError do domínio para o ToolError que o MCP SDK espera.

    Sem isso o cliente MCP só veria "Error executing tool X" — a mensagem real
    (ex. "Product 999 not found") ficaria escondida, só o traceback iria pro log.
    """
    try:
        yield
    except NotFoundError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
async def get_product(product_id: int) -> ProductRead:
    """Busca um produto pelo id. Levanta erro se o produto não existir."""
    async with AsyncSessionLocal() as session:
        service = get_product_service(session)
        with _as_tool_error():
            product = await service.get_by_id(product_id)
        return ProductRead.model_validate(product)


@mcp.tool()
async def get_product_stock(product_id: int) -> int:
    """Devolve a quantidade em estoque de um produto. Levanta erro se não existir."""
    async with AsyncSessionLocal() as session:
        service = get_product_service(session)
        with _as_tool_error():
            return await service.get_stock(product_id)


@mcp.tool()
async def search_products(
    query: str | None = None,
    category: str | None = None,
    max_price: float | None = None,
    min_ram_gb: int | None = None,
    in_stock: bool | None = None,
) -> list[ProductRead]:
    """Busca produtos por texto, categoria, preço máximo, RAM mínima e estoque.

    Todos os filtros são opcionais e se combinam entre si (AND). query busca em
    nome, descrição e marca, case-insensitive. Sem resultados não é erro: devolve
    lista vazia.
    """
    async with AsyncSessionLocal() as session:
        service = get_product_service(session)
        products = await service.search(
            search=query,
            category=category,
            max_price=Decimal(str(max_price)) if max_price is not None else None,
            min_ram_gb=min_ram_gb,
            in_stock=in_stock,
        )
        return [ProductRead.model_validate(p) for p in products]


@mcp.tool()
async def get_order(order_id: int) -> OrderRead:
    """Busca um pedido pelo id, com seus itens. Levanta erro se não existir."""
    async with AsyncSessionLocal() as session:
        service = get_order_service(session)
        with _as_tool_error():
            order = await service.get_by_id(order_id)
        return OrderRead.model_validate(order)


@mcp.tool()
async def search_orders(
    status: OrderStatus | None = None,
    customer_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[OrderRead]:
    """Busca pedidos por status, cliente e intervalo de criação (created_at).

    Todos os filtros são opcionais e se combinam entre si (AND). Sem resultados
    não é erro: devolve lista vazia.
    """
    async with AsyncSessionLocal() as session:
        service = get_order_service(session)
        orders = await service.search(
            status=status, customer_id=customer_id, date_from=date_from, date_to=date_to
        )
        return [OrderRead.model_validate(o) for o in orders]


@mcp.tool()
async def check_order_status(order_id: int) -> OrderStatusRead:
    """Verifica o status de um pedido, incluindo se está atrasado (is_late).

    Levanta erro se o pedido não existir.
    """
    async with AsyncSessionLocal() as session:
        service = get_order_service(session)
        with _as_tool_error():
            return await service.check_status(order_id)


@mcp.tool()
async def get_customer(customer_id: int) -> CustomerRead:
    """Busca um cliente pelo id. Levanta erro se não existir."""
    async with AsyncSessionLocal() as session:
        service = get_customer_service(session)
        with _as_tool_error():
            customer = await service.get_by_id(customer_id)
        return CustomerRead.model_validate(customer)


@mcp.tool()
async def search_customers(
    name: str | None = None,
    email: str | None = None,
) -> list[CustomerRead]:
    """Busca clientes por nome e/ou email, parcial e case-insensitive.

    Filtros se combinam entre si (AND). Sem resultados não é erro: devolve lista
    vazia.
    """
    async with AsyncSessionLocal() as session:
        service = get_customer_service(session)
        customers = await service.search(name=name, email=email)
        return [CustomerRead.model_validate(c) for c in customers]


@mcp.tool()
async def get_customer_orders(
    customer_id: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[OrderRead]:
    """Lista os pedidos de um cliente, opcionalmente filtrados por intervalo de data.

    Levanta erro se o cliente não existir.
    """
    async with AsyncSessionLocal() as session:
        service = get_order_service(session)
        with _as_tool_error():
            orders = await service.get_customer_orders(customer_id, date_from=date_from, date_to=date_to)
        return [OrderRead.model_validate(o) for o in orders]


@mcp.resource("catalog://categories", mime_type="application/json")
async def list_categories() -> list[CategoryRead]:
    """Lista todas as categorias de produto cadastradas."""
    async with AsyncSessionLocal() as session:
        service = get_category_service(session)
        categories = await service.list_all()
        return [CategoryRead.model_validate(c) for c in categories]


@mcp.prompt()
def order_status_prompt(order_id: int) -> str:
    """Template de prompt: pedir pro modelo checar e explicar o status de um pedido."""
    return (
        f"Chame a tool check_order_status para o pedido {order_id} e resuma o "
        "resultado para o cliente em linguagem simples, mencionando claramente "
        "se o pedido está atrasado (is_late) ou não."
    )


if __name__ == "__main__":
    mcp.run()
