class SFNotIncludedError(Exception):
    """
    Exception raised when a sentence fragment is not included in the SF list.
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class EFNotSupportedError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
