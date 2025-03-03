import inspect
import typing

from typing import Callable, Annotated, Any

from data_types import Parameter, DecoratedEntity, Qualifier
from exceptions import UnspecifiedParameterTypeError


def inject(_entity: Callable):
    entity = _parse_entity(_entity)
    print(entity)
    return _entity


def _parse_entity(entity: Callable):
    signature = inspect.signature(entity)

    params_set = set()
    for param in signature.parameters.values():
        if param.annotation is param.empty:
            raise UnspecifiedParameterTypeError(
                entity_name=entity.__name__,
                param_name=param.name
            )

        param_annotation = param.annotation
        param_qualifier = Qualifier.default()

        if typing.get_origin(param_annotation) is Annotated:
            args = typing.get_args(param_annotation)
            _type = args[0]
            hint = args[1]
            if isinstance(hint, Qualifier):
                param_annotation = _type
                param_qualifier = hint

        params_set.add(
            Parameter(
                name=param.name,
                type=param_annotation,
                default_value=param.default if param.default is not param.empty else None,
                qualifier=param_qualifier
            )
        )

    return DecoratedEntity(
        name=entity.__name__,
        parameters=params_set,
        return_annotation=signature.return_annotation,
    )