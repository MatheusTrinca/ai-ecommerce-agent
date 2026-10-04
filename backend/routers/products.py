from decimal import Decimal

from fastapi import APIRouter, Depends

from backend.schemas.product import ProductRead
from backend.services.product_service import ProductService, get_product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
async def search_products(
    search: str | None = None,
    category: str | None = None,
    max_price: Decimal | None = None,
    service: ProductService = Depends(get_product_service),
):
    return await service.search(search=search, category=category, max_price=max_price)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_id(product_id)
