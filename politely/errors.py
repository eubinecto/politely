class EFNotIncludedError(Exception):
    def __init__(self, joined: str):
        self.joined = joined

    def __str__(self) -> str:
        return f"Some sentences do not end with a valid ending: `{self.joined}`"


class EFNotSupportedError(Exception):
    def __init__(self, joined: str):
        self.joined = joined

    def __str__(self) -> str:
        return f"The politely Styler does not support the ending(s): `{self.joined}`"
