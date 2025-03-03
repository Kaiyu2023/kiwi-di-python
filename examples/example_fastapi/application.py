from easy_di import inject
from examples.example_fastapi.services.product_service import ProductService

@inject
def application() -> None:
    pass

if __name__ == '__main__':
    application()