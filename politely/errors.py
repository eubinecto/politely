import re
from typing import List
from politely.rules import RULES


class SFNotIncludedError(Exception):
    """
    Exception raised when a sentence fragment is not included in the SF list.
    """

    def __init__(self, out: str):
        self.out = out

    def __str__(self) -> str:
        return "Sentence does not include a SF:\n" + "\n".join(self.out)


class EFNotSupportedError(Exception):
    def __init__(self, out: str):
        self.out = out

    def __str__(self) -> str:
        return "EF is not supported:\n" + "\n".join(self.out)
