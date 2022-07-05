import re

import requests  # noqa
import pandas as pd  # noqa
from typing import Any
from politely import HONORIFICS, DEL
from politely.errors import EFNotIncludedError, EFNotSupportedError
from functools import wraps
from politely.fetchers import fetch_kiwi


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        # get the function signature
        names = f.__code__.co_varnames[: f.__code__.co_argcount]
        args[0].logs[f.__name__] = {"in": dict(zip(names, args)), "out": args[0].out}
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
    def __call__(self, text: str, politeness: int) -> str:
        """
        style a sentence with the given politeness (1, 2, 3)
        """
        self.setup().preprocess(text).analyze().check().honorify(politeness).conjugate()
        return self.out

    def setup(self):
        """
        reset the out and clear all the logs,
        """
        self.out = None
        self.logs.clear()
        self.logs.update({"conjugations": set(), "honorifics": set()})
        return self

    def preprocess(self, text: str):
        self.out = (
            text.strip()
        )  # khaiii model is sensitive to empty spaces, so we should get rid of it.
        if not self.out.endswith("?") and not self.out.endswith("!"):
            self.out = (
                self.out + "." if not self.out.endswith(".") else self.out
            )  # for accurate pos-tagging
        return self

    @log
    def analyze(self):
        self.out: str
        self.out = self.kiwi.tokenize(self.out)
        self.out = DEL.join([token.tagged_form for token in self.out])
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        self.out: str
        # raise exceptions only if you are in debug mode
        if self.debug:
            # assumption 1: every sentence should end with SF (., !, ?)
            # TODO:
            # assumption 2: every sentence must include more than 1 EF's
            if "EF" not in self.out:
                raise EFNotIncludedError(self.out)
            # assumption 3: all EF's should be supported by politely.
            # TODO: does not really check if "all" EFs are supported by politely. This is fine for now, but should be fixed in the future.
            if not any([self.matches(pattern, self.out) for pattern in HONORIFICS if "EF" in pattern]):
                raise EFNotSupportedError(self.out)
        return self

    @log
    def honorify(self, politeness: int):
        self.out: str
        for pattern in HONORIFICS.keys():
            if self.matches(pattern, self.out):
                honorific = HONORIFICS[pattern][politeness]
                self.out = re.sub(pattern, honorific, self.out)
                self.logs["honorifics"].add((pattern, honorific))
        return self

    @log
    def conjugate(self):
        """
        Progressively conjugate morphemes from left to right.
        """
        self.out: str
        morphs = [
            (token.split("/")[0], token.split("/")[1]) for token in self.out.split(DEL)
        ]
        self.out = self.kiwi.join(morphs)
        return self

    @staticmethod
    def matches(pattern: str, string: str) -> bool:
        return (
            True if re.findall(rf"(^|.*{DEL}){pattern}({DEL}.*|$)", string) else False
        )
