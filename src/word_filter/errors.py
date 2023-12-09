class TooManyWeights(Exception):
    def __init__(self, found: int, max: int):
        self.found = found
        self.max = max

    def __str__(self):
        return (
            f"Error: too many weights present - found {self.found}, max is {self.max}"
        )


class UnexpectedNegativeValue(Exception):
    def __init__(self, field: str, value: int):
        self.field = field
        self.value = value

    def __str__(self):
        return f"Error: '{self.field}' cannot have negative numbers; found={self.value}"


class InternalError(Exception):
    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return f"Internal Error: {self.error}"

