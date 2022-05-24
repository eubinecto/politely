import inspect
import re
import requests  # noqa
import pandas as pd  # noqa
from khaiii.khaiii import KhaiiiApi
from typing import Any, Tuple, Set
from politely.fetchers import fetch_honorifics, fetch_rules
from politely.errors import EFNotIncludedError, EFNotSupportedError
from multipledispatch import dispatch
from dataclasses import dataclass, field
from politely.hangul import conjugate


class Styler:
    """
    A rule-based Korean Politeness Styler
    """
    @dataclass
    class Logs:
        args: dict = field(default_factory=dict)
        case: dict = field(default_factory=dict)
        steps: list = field(default_factory=list)
        honorifics: Set[Tuple[str, str]] = field(default_factory=set)
        conjugations: Set[Tuple[str, str, str, str]] = field(default_factory=set)
    # class-owned attributes
    RULES: dict = fetch_rules()
    HONORIFICS: dict = fetch_honorifics()

    def __init__(self):
        # object-owned attributes
        self.khaiii = KhaiiiApi()
        self.out: Any = None
        self.logs = self.Logs()

    @dispatch(str, str, str)
    def __call__(self, sent: str, listener: str, environ: str) -> str:
        """
        First way of using Styler - have Styler determine the politeness for you.
        """
        self.clear() \
            .save() \
            .determine(listener, environ) \
            .process(sent, self.logs.case['politeness'])
        return self.out

    @dispatch(str, int)
    def __call__(self, sent: str, politeness: int) -> str:
        """
        The other way of using Styler - you know your politeness already, just use this as a styler per se.
        This would more suitable than the first __call__ for  e.g. augmentation of data purposes.
        """
        self.clear() \
            .save() \
            .process(sent, politeness)
        return self.out

    def process(self, sent: str, politeness: int):
        """
        The common steps for all __call__'s.
        """
        self.preprocess(sent) \
            .analyze() \
            .check() \
            .log() \
            .honorify(politeness) \
            .log() \
            .conjugate() \
            .log()
        return self

    def save(self):
        """
        save whatever arguments that were provided to __call__
        """
        f_back = inspect.currentframe().f_back
        args = inspect.getargvalues(f_back)
        self.logs.args.update(args.locals)
        return self

    def clear(self):
        """
        clear all logs
        """
        self.logs.args.clear()
        self.logs.steps.clear()
        self.logs.honorifics.clear()
        self.logs.conjugations.clear()
        return self

    def log(self):
        """
        log the current out
        """
        self.logs.steps.append(self.out)
        return self

    def determine(self, listener: str, environ: str):
        """
        determine the case from the rules.
        """
        self.logs.case = self.RULES[listener][environ]
        return self

    def preprocess(self, sent: str):
        self.out = sent.strip()  # khaiii model is sensitive to empty spaces, so we should get rid of it.
        if not self.out.endswith("?") and not self.out.endswith("!"):
            self.out = self.out + "." if not self.out.endswith(".") else self.out  # for accurate pos-tagging
        return self

    def analyze(self):
        tokens = self.khaiii.analyze(self.out)
        self.out = tokens
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        efs = [
            "+".join(map(str, token.morphs))
            for token in self.out
            if "EF" in "+".join(map(str, token.morphs))
        ]
        # assumption 1: the sentence must include more than 1 EF's
        if not efs:
            raise EFNotIncludedError("|".join(["+".join(map(str, token.morphs)) for token in self.out]))
        # assumption 2: all EF's should be supported by KPS.
        for ef in efs:
            for pattern in self.HONORIFICS.keys():
                if self.matched(pattern, ef):
                    break
            else:
                raise EFNotSupportedError(ef)
        return self

    def honorify(self, politeness: int):
        lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in self.out]
        self.out = list()
        for lex, morphs in lex2morphs:
            tuned = "+".join(morphs)
            for pattern in self.HONORIFICS.keys():
                if self.matched(pattern, tuned):
                    honorific = self.HONORIFICS[pattern][politeness]
                    tuned = tuned.replace(pattern, honorific)
                    self.logs.honorifics.add((pattern, honorific))
            # if something has changed, then go for it, but otherwise just use the lex.
            before = [morph.split("/")[0] for morph in morphs]
            after = [morph.split("/")[0] for morph in tuned.split("+")]
            if "".join(before) != "".join(after):
                self.out.append(after)
            else:
                self.out.append(lex)
        return self

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
                    left, log = conjugate(left, right)
                    self.logs.conjugations.add(log)
                out.append(left)
            else:
                out.append(chunk)
        self.out = " ".join(out)
        return self

    # --- accessing options --- #
    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def environs(self):
        return pd.DataFrame(self.RULES).transpose().columns

    # --- supporting methods --- #
    @staticmethod
    def matched(pattern: str, string: str) -> bool:
        return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False
