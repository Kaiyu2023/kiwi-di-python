import logging

from easy_di import component
from entity_registry import ComponentRegistry
from examples.example_simple_app.services.product_service import ProductService

@component
def application(name: str = "") -> None:
    print(f"Application function called with {name}")

if __name__ == '__main__':
    logging.getLogger("ComponentRegistry").setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logging.getLogger("ComponentRegistry").addHandler(ch)
    application("TEST")
    ComponentRegistry.wire_components()
    print("Instantiated:")
    print(ComponentRegistry._component_instances)
    print("Waiting list:")
    print(ComponentRegistry._waiting_list)
    print("signal list:")
    print(ComponentRegistry._signal_dict)
