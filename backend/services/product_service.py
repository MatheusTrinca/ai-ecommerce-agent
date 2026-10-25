from decimal import Decimal

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.models.product import Product
from backend.repositories.category_repository import CategoryRepository
from backend.repositories.product_repository import ProductRepository
from backend.services.exceptions import NotFoundError


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._product_repository = product_repository
        self._category_repository = category_repository

    async def get_by_id(self, product_id: int) -> Product:
        product = await self._product_repository.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")
        return product

    async def search(
        self,
        search: str | None = None,
        category: str | None = None,
        max_price: Decimal | None = None,
        min_ram_gb: int | None = None,
        in_stock: bool | None = None,
    ) -> list[Product]:
        category_id: int | None = None
        if category is not None:
            category_obj = await self._category_repository.get_by_name(category)
            if category_obj is None:
                return []
            category_id = category_obj.id

        return await self._product_repository.search(
            search=search,
            category_id=category_id,
            max_price=max_price,
            min_ram_gb=min_ram_gb,
            in_stock=in_stock,
        )

    async def get_stock(self, product_id: int) -> int:
        product = await self.get_by_id(product_id)
        return product.stock


def get_product_service(session: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(session), CategoryRepository(session))
