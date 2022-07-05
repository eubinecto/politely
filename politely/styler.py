import re
import requests  # noqa
import pandas as pd  # noqa
from typing import Any, List
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
        """
        I know it is inefficient to tokenize twice (once here, and one more in analyze),
        But I have to leave this here. Work on the speed later.
        """
        # first, split into sentences
        out = [sent.text.strip() for sent in self.kiwi.split_into_sents(text)]
        # second, append a period if it does not have any valid SF
        self.out = [re.sub(r"([^!?.]+)$", r"\1.", sent) for sent in out]
        return self

    @log
    def analyze(self):
        self.out: List[str]
        self.out = [
            DEL.join([token.tagged_form for token in self.kiwi.tokenize(sent)])
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
            # assumption 1: every sentence should end with SF. It should be one of: (., !, ?)
            # TODO:
            # assumption 2: every sentence must include more than 1 EF's
            if not all(["EF" in joined for joined in self.out]):
                raise EFNotIncludedError("|".join(self.out))
            # assumption 3: all EF's should be supported by politely.
            if not all([any([self.matches(pattern, joined) for pattern in HONORIFICS.keys() if "EF" in pattern]) for joined in self.out]):
                raise EFNotSupportedError("|".join(self.out))
        return self

    @log
    def honorify(self, politeness: int):
        self.out: List[str]
        self.out = DEL.join(self.out)
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
