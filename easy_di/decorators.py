import inspect
import typing

from typing import Callable, Annotated, Any

from data_types import Parameter, ComponentMetadata, Qualifier, DEFAULT_QUALIFIER, NO_DEFAULT_VALUE
from entity_registry import ComponentRegistry
from exceptions import UnspecifiedParameterTypeError


def component(_component: Callable, qualifier: str = DEFAULT_QUALIFIER) -> Callable:
    entity_metadata = _get_metadata(
        _component=_component,
        component_qualifier=qualifier
    )
    ComponentRegistry.register_component(entity_metadata)
    return _component

def _get_metadata(_component: Callable, component_qualifier: str) -> ComponentMetadata:
    signature = inspect.signature(_component)
    component_name = f"{_component.__module__}.{_component.__name__}"

    params_set = set()
    for param in signature.parameters.values():
        if param.annotation is param.empty:
            raise UnspecifiedParameterTypeError(
                component_name=component_name,
                param_name=param.name
            )

        param_annotation = param.annotation
        param_qualifier = DEFAULT_QUALIFIER

        if typing.get_origin(param_annotation) is Annotated:
            args = typing.get_args(param_annotation)
            _type = args[0]
            hint = args[1]
            if isinstance(hint, Qualifier):
                param_annotation = _type
                param_qualifier = hint.name

        params_set.add(
            Parameter(
                name=param.name,
                type=f"{param_annotation.__module__}.{param_annotation.__name__}",
                default_value=param.default if param.default is not param.empty else NO_DEFAULT_VALUE,
                qualifier=param_qualifier
            )
        )

    return ComponentMetadata(
        name=component_name,
        parameters=params_set,
        return_annotation=signature.return_annotation,
        entity_qualifier=component_qualifier,
        instantiate_func=_component
    )