from collections.abc import Callable
from typing import Annotated

from data_types import Qualifier
from easy_di import inject
from examples.example_fastapi.domain import Product
from examples.example_fastapi.repository.product_repository import ProductRepository

@inject
class ProductService:

    def __init__(self, product_repository: ProductRepository, test_value: Annotated[ProductRepository, Qualifier("TestQualifier")] = 0, call: Callable[[str], None] = None) -> None:
        self._product_repository = product_repository

    def get_products(self) -> list[Product]:
        return self._product_repository.get_products()
