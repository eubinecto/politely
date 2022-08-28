import itertools
import re
from copy import copy
import requests  # noqa
import pandas as pd  # noqa
from typing import Any, List
from functools import wraps
from politely.errors import EFNotSupportedError, SFNotIncludedError
from politely.fetchers import fetch_kiwi, fetch_scorer
from politely import RULES, SEP, TAG, MASK, NULL, SELF


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
        self.scorer = fetch_scorer()
        self.debug = debug
        self.out: Any = None
        self.logs = dict()

    @log
    def __call__(self, sents: List[str], politeness: int) -> List[str]:
        """
        Style a sentence with the given politeness (0, 1, 2)
        """
        self.setup() \
            .preprocess(sents) \
            .analyze() \
            .check() \
            .honorify(politeness) \
            .guess() \
            .conjugate()
        return self.out

    def setup(self):
        """
        Reset the out and clear all the logs,
        """
        self.out = None
        self.logs.clear()
        self.logs.update({"conjugations": set(), "honorifics": set()})
        return self

    def preprocess(self, sents: List[str]):
        """
        Make sure each sentence ends with a period, if it does not end with any SF.
        We do this to increase the accuracy of `kiwi.join`.
        """
        self.out = [re.sub(r"([^!?.]+)$", r"\1.", sent.strip()) for sent in sents]
        return self

    @log
    def analyze(self):
        """
        Analyze the sentence and generate the output.
        """
        self.out: List[str]
        self.out = [
            SEP.join(
                [f"{token.form}{TAG}{token.tag}" for token in self.kiwi.tokenize(sent)]
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
            if not all(["SF" in morphs for morphs in self.out]):
                raise SFNotIncludedError(self.out)
            # assumption 2: all EF's should be supported by politely.
            if not all([
                any([re.search(regex, morphs) for regex in RULES])
                for morphs in self.out
                if "EF" in morphs
            ]):
                raise EFNotSupportedError(self.out)
        return self

    @log
    def honorify(self, politeness: int):
        """
        Determines all the candidates that would properly honorify the sentence.
        Do this by chain-conjugating sets.
        """
        self.out: List[str]
        out = list()
        for morphs in self.out:
            morph2honorifics = {}
            for regex in RULES:
                match = re.search(regex, morphs)
                if match:
                    key = match.group(MASK)
                    honorifics = {honorific.replace(SELF, key)
                                  for honorific in RULES[regex][politeness]}
                    # chain-conjugate the honorifics
                    morph2honorifics[key] = morph2honorifics.get(key, honorifics) & honorifics
            # product it
            candidates = itertools.product(*[
                morph2honorifics.get(morph, {morph, })
                for morph in morphs.split(SEP)
            ])
            # preprocess it
            candidates = [
                [morph.split(SEP) for morph in candidate if morph != NULL]
                for candidate in candidates
            ]
            # flatten it
            candidates = [
                list(itertools.chain(*candidate))
                for candidate in candidates
            ]
            out.append(candidates)
        # a list of candidates
        self.out = out
        return self

    @log
    def guess(self):
        """
        Guess the best candidates using the `scorer`.
        """
        self.out: List[List[List[str]]]
        self.out = [
            sorted(candidates, key=lambda x: self.scorer(x), reverse=True)[0]
            for candidates in self.out
        ]
        return self

    @log
    def conjugate(self):
        """
        Conjugate the guesses to get the final result.
        """
        self.out: List[List[str]]
        self.out = [
            self.kiwi.join([tuple(morph.split(TAG)) for morph in morphs])  # noqa
            for morphs in self.out
        ]
        return self
