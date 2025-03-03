from copy import deepcopy
from decimal import Decimal

from examples.example_fastapi.domain import Product
from easy_di import inject

@inject
class ProductRepository:

    def __init__(self) -> None:
        self._products = [
            Product(name="Apple", price=Decimal(0.99)),
            Product(name="Banana", price=Decimal(1.99)),
            Product(name="Avocado", price=Decimal(2.99)),
        ]

    def get_products(self) -> list[Product]:
        return deepcopy(self._products)