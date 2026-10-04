from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.models.customer import Customer
from backend.repositories.customer_repository import CustomerRepository
from backend.services.exceptions import NotFoundError


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self._customer_repository = customer_repository

    async def get_by_id(self, customer_id: int) -> Customer:
        customer = await self._customer_repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")
        return customer


def get_customer_service(session: AsyncSession = Depends(get_db)) -> CustomerService:
    return CustomerService(CustomerRepository(session))
