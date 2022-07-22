import re
from copy import copy
import requests  # noqa
import pandas as pd  # noqa
from typing import Any, List, Union, Tuple
from functools import wraps
from politely.errors import EFNotSupportedError, SFNotIncludedError
from politely.fetchers import fetch_kiwi, fetch_scorer
from politely import RULES, SEP, TAG, NULL


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
        reset the out and clear all the logs,
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
        Use Kiwi to analyze the morphemes of the sentence.
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
        Using the chained conjunction algorithm, determine the candidates that would
        properly honorify the sentence.
        """
        self.out: List[str]
        out = list()
        for joined in self.out:
            morph2honorifics = {}
            for regex in RULES:
                match = re.search(regex, joined)
                if match:
                    key = match.group("mask")
                    honorifics = {honorific.replace(r"\g<mask>", key)
                                  for honorific in RULES[regex][politeness]}
                    morph2honorifics[key] = morph2honorifics.get(key, honorifics) & honorifics
            candidates = [
                morph2honorifics.get(morph, morph)
                for morph in joined.split(SEP)
            ]
            out.append(candidates)
        self.out = out
        return self

    @log
    def guess(self):
        """
        Now that we have the candidates, we should guess which one
        is the correct one.
        """
        self.out: List[List[Union[str, set]]]
        out = list()
        for candidates in self.out:
            guess = list()
            for candidate in candidates:
                if isinstance(candidate, set):
                    # can we do better than random choice?
                    best = sorted(list(candidate), key=lambda x: self.scorer(x), reverse=True)[0]
                    if best != NULL:
                        for morph2pos in best.split(SEP):
                            guess.append(tuple(morph2pos.split(TAG)))
                else:
                    guess.append(tuple(candidate.split(TAG)))
            out.append(guess)
        self.out = out
        return self

    @log
    def conjugate(self):
        """
        Conjugate the guesses to get the final result.
        """
        self.out: List[List[Tuple[str, str]]]
        self.out = [
            self.kiwi.join(morphs)  # noqa
            for morphs in self.out
        ]
        return self
