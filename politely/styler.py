import re
import requests  # noqa
import pandas as pd  # noqa
from khaiii.khaiii import KhaiiiApi
from typing import Any
from politely import HONORIFICS
from politely.errors import EFNotIncludedError, EFNotSupportedError
from politely.hangle import conjugate
from functools import wraps


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        # get the function signature
        names = f.__code__.co_varnames[: f.__code__.co_argcount]
        args[0].logs[f.__name__] = {"in": dict(zip(names, args)), "out": args[0].out}
        return out

    return wrapper


def matched(pattern: str, string: str) -> bool:
    return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False


class Styler:
    """
    A rule-based Korean Politeness Styler
    """

    def __init__(self):
        # object-owned attributes
        self.khaiii = KhaiiiApi()
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
        tokens = self.khaiii.analyze(self.out)
        self.out = tokens
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        efs = [
            "+".join(map(str, token.morphs)) for token in self.out if "EF" in "+".join(map(str, token.morphs))
        ]
        # assumption 1: the sentence must include more than 1 EF's
        if not efs:
            raise EFNotIncludedError("|".join(["+".join(map(str, token.morphs)) for token in self.out]))
        # assumption 2: all EF's should be supported by KPS.
        for ef in efs:
            for pattern in HONORIFICS:
                if matched(pattern, ef):
                    break
            else:
                raise EFNotSupportedError(ef)
        return self

    @log
    def honorify(self, politeness: int):
        lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in self.out]
        self.out = list()
        for lex, morphs in lex2morphs:
            tuned = "+".join(morphs)
            for pattern in HONORIFICS.keys():
                if matched(pattern, tuned):
                    honorific = HONORIFICS[pattern][politeness]
                    tuned = tuned.replace(pattern, honorific)
                    self.logs["honorifics"].add((pattern, honorific))
            # if something has changed, then go for it, but otherwise just use the lex.
            before = [morph.split("/")[0] for morph in morphs]
            after = [morph.split("/")[0] for morph in tuned.split("+")]
            if "".join(before) != "".join(after):
                self.out.append(after)
            else:
                self.out.append(lex)
        return self

    @log
    def conjugate(self):
        """
        Progressively conjugate morphemes from left to right.
        """
        out = list()
        for chunk in self.out:
            if isinstance(chunk, list):
                left = chunk[0]
                for i in range(len(chunk) - 1):
                    right = chunk[i + 1]
                    left, logs = conjugate(left, right)
                    self.logs["conjugations"].add(logs)
                out.append(left)
            else:
                out.append(chunk)
        self.out = " ".join(out)
        return self
