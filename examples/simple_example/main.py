from animal import AnimalFamily
from registry import ComponentRegistry

if __name__ == '__main__':
    ComponentRegistry().wire_components()
    print("Instances", ComponentRegistry()._component_instances)
    print("Waiting", ComponentRegistry()._waiting_list)
    print("Signal", ComponentRegistry()._signal_dict)