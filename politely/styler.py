import re
from copy import copy

import requests  # noqa
import pandas as pd  # noqa
from typing import Any, List
from politely import HONORIFICS, DLM, SEP
from politely.errors import EFNotSupportedError, SFNotIncludedError
from functools import wraps
from politely.fetchers import fetch_kiwi


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        # get the function signature
        names = f.__code__.co_varnames[: f.__code__.co_argcount]
        args[0].logs[f.__name__] = {"in": dict(zip(names, args)), "out": copy(args[0].out)}
        return out

    return wrapper


class Styler:
    """
    A rule-based Korean Politeness Styler
    """

    def __init__(self, debug: bool = False):
        # object-owned attributes
        self.kiwi = fetch_kiwi()
        self.debug = debug
        self.out: Any = None
        self.logs = dict()

    @log
    def __call__(self, sents: List[str], politeness: int) -> List[str]:
        """
        style a sentence with the given politeness (1, 2, 3)
        """
        self.setup().preprocess(sents).analyze().check().honorify(politeness).conjugate()
        return self.out

    def setup(self):
        """
        reset the out and clear all the logs,
        """
        self.out = None
        self.logs.clear()
        self.logs.update({"conjugations": set(), "honorifics": set()})
        return self

    def preprocess(self, sents: List[str]):
        """
        I know it is inefficient to tokenize twice (once here, and one more in analyze),
        But I have to leave this here and work on the speed later.
        """
        self.out = [re.sub(r"([^!?.]+)$", r"\1.", sent.strip()) for sent in sents]
        return self

    @log
    def analyze(self):
        self.out: List[str]
        self.out = [
            DLM.join(
                [f"{token.form}{SEP}{token.tag}" for token in self.kiwi.tokenize(sent)]
            )
            for sent in self.out
        ]
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        self.out: List[str]
        # raise exceptions only if you are in debug mode
        if self.debug:
            # assumption 1: every sentence should end with a valid SF. It should be one of: (., !, ?)
            if not all(["SF" in joined for joined in self.out]):
                raise SFNotIncludedError(
                    "The following sentences do not include a SF:\n"
                    + "\n".join([joined for joined in self.out if "SF" not in joined])
                )
            # assumption 2: all EF's should be supported by politely.
            if not all(
                [
                    any(
                        [self.matches(pattern, joined) for pattern in HONORIFICS.keys()]
                    )
                    for joined in self.out
                    if "EF" in joined
                ]
            ):
                raise EFNotSupportedError(
                    "Styler does not support the ending(s):\n"
                    + "\n".join(
                        [
                            joined
                            for joined in self.out
                            if not any(
                                [
                                    self.matches(pattern, joined)
                                    for pattern in HONORIFICS.keys()
                                ]
                            )
                        ]
                    )
                )
        return self

    @log
    def honorify(self, politeness: int):
        self.out: List[str]
        for idx in range(len(self.out)):
            for pattern in HONORIFICS.keys():
                if self.matches(pattern, self.out[idx]):
                    honorific = HONORIFICS[pattern][politeness]
                    self.out[idx] = re.sub(pattern, honorific, self.out[idx])
                    self.logs["honorifics"].add((pattern, honorific))
        return self

    @log
    def conjugate(self):
        """
        Progressively conjugate morphemes from left to right.
        """
        self.out: List[str]
        self.out = [
            [(token.split(SEP)[0], token.split(SEP)[1]) for token in joined.split(DLM) if SEP in token]
            for joined in self.out
        ]
        self.out = [
            self.kiwi.join(morphs)
            for morphs in self.out
        ]
        return self

    @staticmethod
    def matches(pattern: str, string: str) -> bool:
        return True if re.match(rf"(^|.*{DLM}){pattern}({DLM}.*|$)", string) else False
