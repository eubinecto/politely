import re
from typing import List
from politely.rules import RULES


class SFNotIncludedError(Exception):
    """
    Exception raised when a sentence fragment is not included in the SF list.
    """

    def __init__(self, out: List[str]):
        self.out = out

    def __str__(self) -> str:
        msg = "The following sentences do not include a SF:\n" \
              + "\n".join([joined for joined in self.out if "SF" not in joined])
        return msg


class EFNotSupportedError(Exception):
    def __init__(self, out: List[str]):
        self.out = out

    def __str__(self) -> str:
        msg = "Styler does not support the ending(s):\n" \
              + "\n".join(
            [
                morphs
                for morphs in self.out
                if not any(
                [
                    re.match(regex, morphs)
                    for regex in RULES
                ]
            )
            ]
        )
        return msg
