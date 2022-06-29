import re
import requests  # noqa
import pandas as pd  # noqa
from _kiwipiepy import Token
from typing import Any, List
from politely import HONORIFICS
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


def matches(pattern: str, string: str) -> bool:
    return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False


class Styler:
    """
    A rule-based Korean Politeness Styler
    """

    def __init__(self):
        # object-owned attributes
        self.kiwi = fetch_kiwi()
        self.out: Any = None
        self.logs = dict()

    @log
    def __call__(self, sent: str, politeness: int) -> str:
        """
        style a sentence with the given politeness (1, 2, 3)
        """
        self.setup().preprocess(sent).analyze().check().honorify(politeness).conjugate()
        return self.out

    def setup(self):
        """
        reset the out and clear all the logs,
        """
        self.out = None
        self.logs.clear()
        self.logs.update({"conjugations": set(), "honorifics": set()})
        return self

    def preprocess(self, sent: str):
        self.out = sent.strip()  # khaiii model is sensitive to empty spaces, so we should get rid of it.
        if not self.out.endswith("?") and not self.out.endswith("!"):
            self.out = self.out + "." if not self.out.endswith(".") else self.out  # for accurate pos-tagging
        return self

    @log
    def analyze(self):
        tokens = self.kiwi.tokenize(self.out)
        self.out = tokens
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        self.out: List[Token]
        self.out = "+".join([token.tagged_form for token in self.out])
        # assumption 1: the sentence must include more than 1 EF's
        if "EF" not in self.out:
            raise EFNotIncludedError(self.out)
        # assumption 2: all EF's should be supported by politely.
        if not any([matches(pattern, self.out) for pattern in HONORIFICS]):
            raise EFNotSupportedError(self.out)
        return self

    @log
    def honorify(self, politeness: int):
        self.out: str
        for pattern in HONORIFICS.keys():
            if matches(pattern, self.out):
                honorific = HONORIFICS[pattern][politeness]
                self.out = self.out.replace(pattern, honorific)
                self.logs["honorifics"].add((pattern, honorific))
        return self

    @log
    def conjugate(self):
        """
        Progressively conjugate morphemes from left to right.
        """
        self.out: str
        morphs = [(token.split("/")[0], token.split("/")[1]) for token in self.out.split("+")]
        self.out = self.kiwi.join(morphs)
        # TODO: how do I log all the rules that have been applied?
        return self
