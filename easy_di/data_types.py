import dataclasses
from typing import Type, Any, Callable


@dataclasses.dataclass(frozen=True)
class Qualifier:
    name: str

DEFAULT_QUALIFIER = "__default_qualifier__"


class _NoDefaultValue:
    pass

NO_DEFAULT_VALUE = _NoDefaultValue()

@dataclasses.dataclass(frozen=True)
class Parameter:
    name: str
    type: str
    default_value: Any | _NoDefaultValue
    qualifier: str


@dataclasses.dataclass
class ComponentMetadata:
    name: str
    parameters: set[Parameter]
    return_annotation: Type
    entity_qualifier: str
    instantiate_func: Callable