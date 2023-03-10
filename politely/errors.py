import re
from typing import List
from politely.rules import RULES


class SFNotIncludedError(Exception):
    """
    An exception raised when a sentence does not include a SF.
    """

    def __init__(self, out: str):
        self.out = out

    def __str__(self) -> str:
        return "Sentence does not include a SF:\n" + "\n".join(self.out)


class EFNotIncludedError(Exception):
    """
    An exception raised when a sentence does not include an EF.
    """

    def __init__(self, out: str):
        self.out = out

    def __str__(self) -> str:
        return "Sentence does not include an EF:\n" + "\n".join(self.out)


class EFNotSupportedError(Exception):
    """
    An exception raised when a sentence includes an EF that is not supported.
    """
    def __init__(self, out: str):
        self.out = out

    def __str__(self) -> str:
        return "EF is not supported:\n" + "\n".join(self.out)
