class EFNotIncludedError(Exception):
    def __init__(self, joined: str):
        self.joined = joined

    def __str__(self) -> str:
        return f"The sentence does not end with any valid endings: `{self.joined}`"


class EFNotSupportedError(Exception):
    def __init__(self, joined: str):
        self.joined = joined

    def __str__(self) -> str:
        return f"The politely Styler does not support the ending(s): `{self.joined}`"
