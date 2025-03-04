from collections.abc import Callable
from typing import Annotated

from data_types import Qualifier
from easy_di import component
from examples.example_simple_app.domain import Product
from examples.example_simple_app.repository.product_repository import ProductRepository

@component
class ProductService:

    def __init__(self, product_repository: ProductRepository, call: Callable[[str], None] = None) -> None:
        self._product_repository = product_repository

    def get_products(self) -> list[Product]:
        return self._product_repository.get_products()
