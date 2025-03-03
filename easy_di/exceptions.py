class UnspecifiedParameterTypeError(RuntimeError):

    def __init__(self, entity_name: str, param_name: str):
        super().__init__(
            f"Cannot wire class/function {entity_name}, parameter type is not specified for {param_name}."
        )