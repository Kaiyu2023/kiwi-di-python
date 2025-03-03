import dataclasses
from typing import Type, Optional, Any



@dataclasses.dataclass(frozen=True)
class Qualifier:
    name: str

    @staticmethod
    def default() -> "Qualifier":
        return Qualifier(name="__default_qualifier__")

@dataclasses.dataclass(frozen=True)
class Parameter:
    name: str
    type: Type
    default_value: Optional[Any]
    qualifier: Qualifier


@dataclasses.dataclass
class DecoratedEntity:
    name: str
    parameters: set[Parameter]
    return_annotation: Type