import dataclasses
from decimal import Decimal


@dataclasses.dataclass
class Product:
    name: str
    price: Decimal
