import dataclasses
import logging
from copy import deepcopy
from typing import Any, Iterable

from data_types import ComponentMetadata, NO_DEFAULT_VALUE
from exceptions import AmbiguousEntityError

logger = logging.getLogger("ComponentRegistry")

@dataclasses.dataclass(frozen=True)
class _ComponentId:
    name: str
    qualifier: str

@dataclasses.dataclass(frozen=True)
class _WaitingListItem:
    metadata: ComponentMetadata
    waiting_on: set[_ComponentId]

class ComponentRegistry:

    _component_metadata: dict[_ComponentId, ComponentMetadata] = {}
    _component_instances: dict[_ComponentId, Any] = {}
    _config_values: dict[str, Any] = {}

    _waiting_list: dict[_ComponentId, _WaitingListItem] = {}
    _signal_dict: dict[_ComponentId, set[_ComponentId]] = {}

    @classmethod
    def components(cls) -> dict[_ComponentId, ComponentMetadata]:
        return deepcopy(cls._component_metadata)

    @classmethod
    def register_component(cls, entity_metadata: ComponentMetadata) -> None:
        entity_id = _ComponentId(
            name=entity_metadata.name,
            qualifier=entity_metadata.entity_qualifier
        )
        if entity_id in cls._component_metadata:
            raise AmbiguousEntityError(name=entity_id.name, qualifier=entity_id.qualifier)
        cls._component_metadata[entity_id] = entity_metadata

    @classmethod
    def load_config_values(cls) -> None:
        raise NotImplementedError()

    @classmethod
    def wire_components(cls) -> None:
        for component_id, metadata in cls._component_metadata.items():
            cls._try_instantiate_component(component_id, metadata)
        # TODO(Kaiyu): Throw when some components cannot be instantiated
        logger.debug("All component instantiated.")

    @classmethod
    def _try_instantiate_component(cls, component_id: _ComponentId, metadata: ComponentMetadata) -> None:
        if len(metadata.parameters) == 0:
            logger.debug("Instantiating %s with no parameters", component_id)
            cls._component_instances[component_id] = metadata.instantiate_func()
            return

        param_values: dict[str, Any] = {}
        unresolved_params: dict[str, _ComponentId] = {}

        for param in metadata.parameters:
            if param.default_value != NO_DEFAULT_VALUE:
                param_values[param.name] = param.default_value
                continue

            # TODO(Kaiyu): Get from config values

            param_component_id = _ComponentId(name=param.type, qualifier=param.qualifier)
            if param_component_id in cls._component_instances:
                param_values[param.name] = cls._component_instances[param_component_id]
                continue

            unresolved_params[param.name] = param_component_id

        if len(unresolved_params) == 0:
            logger.debug("Instantiating %s with all its parameters", component_id)
            cls._component_instances[component_id] = metadata.instantiate_func(**param_values)
            if component_id in cls._waiting_list:
                cls._waiting_list.pop(component_id)
            cls._signal_waiting_list(instantiated_component=component_id)
        else:
            logger.debug("Put %s on waiting list, waiting on %s", component_id, unresolved_params)
            cls._waiting_list[component_id] = _WaitingListItem(
                metadata=metadata, waiting_on=set(unresolved_params.values())
            )
            cls._add_to_signal_dict(component_id, unresolved_params.values())

    @classmethod
    def _add_to_signal_dict(cls, component_id: _ComponentId, unresolved_params: Iterable[_ComponentId]) -> None:
        for param_component_id in unresolved_params:
            if param_component_id in cls._signal_dict:
                cls._signal_dict[param_component_id].add(component_id)
            else:
                cls._signal_dict[param_component_id] = {component_id}

    @classmethod
    def _signal_waiting_list(cls, instantiated_component: _ComponentId) -> None:
        if instantiated_component not in cls._signal_dict:
            return
        for component_to_signal in cls._signal_dict[instantiated_component]:
            if (component_to_signal in cls._waiting_list
                and instantiated_component in cls._waiting_list[component_to_signal].waiting_on):
                cls._try_instantiate_component(
                    component_id=component_to_signal,
                    metadata=cls._waiting_list[component_to_signal].metadata
                )