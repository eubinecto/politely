

class EFNotSupportedError(Exception):
    def __init__(self, ef: str):
        self.ef = ef

    def __str__(self) -> str:
        return f"The politely Styler does not support the ending: `{self.ef}`"


class EFNotIncludedError(Exception):

    def __init__(self, sent: str):
        self.sent = sent

    def __str__(self) -> str:
        return f"The sentence does not end with a valid ending: `{self.sent}`"
