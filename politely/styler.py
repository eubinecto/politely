import itertools
import re
from copy import copy
from typing import Any, List, Tuple
from functools import wraps
from politely.errors import EFNotSupportedError, SFNotIncludedError
from politely.fetchers import fetch_kiwi, fetch_scorer
from politely import RULES, SEP, TAG, MASK, NULL, SELF, CASUAL, POLITE, FORMAL


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
    def __init__(self, strict: bool = False):
        # object-owned attributes
        self.kiwi = fetch_kiwi()
        self.scorer = fetch_scorer()
        self.strict = strict
        self.out: Any = None
        self.logs = dict()

    @log
    def __call__(self, sent: str, politeness: int) -> str:
        """
        Style a sentence with the given politeness (0, 1, 2)
        """
        self.setup() \
            .preprocess(sent) \
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

    def preprocess(self, sent: str):
        """
        Make sure each sentence ends with a period, if it does not end with any SF.
        We do this to increase the accuracy of `kiwi.join`.
        """
        self.out = re.sub(r"([^!?.]+)$", r"\1.", sent.strip())
        return self

    @log
    def analyze(self):
        """
        Analyze the sentence and generate the output.
        """
        self.out: str
        self.out = [f"{token.form}{TAG}{token.tag}" for token in self.kiwi.tokenize(self.out)]
        self.out = SEP.join(self.out)  # to match with the format of the rules
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        self.out: str
        # raise exceptions only if you are in debug mode
        if self.strict:
            # assumption 1: every sentence should end with a valid SF. It should be one of: (., !, ?)
            if "SF" not in self.out:
                raise SFNotIncludedError(self.out)
            # assumption 2: all EF's should be supported by politely.
            if not all([
                any([re.search(pattern, pair) for pattern in RULES.keys()])
                for pair in self.out.split(SEP)
                if "EF" in pair
            ]):
                raise EFNotSupportedError(self.out)
        return self

    @log
    def honorify(self, politeness: int):
        """
        Determines all the candidates that would properly honorify the sentence.
        Do this by chain-conjugating sets.
        """
        self.out: str
        pair2honorifics = {}
        for pattern in RULES.keys():
            match = re.search(pattern, self.out)
            if match:
                matched_pair = match.group(MASK)
                honorifics = {honorific.replace(SELF, matched_pair) for honorific in RULES[pattern][politeness]}
                # progressively narrow down honorifics
                pair2honorifics[matched_pair] = pair2honorifics.get(matched_pair, honorifics) & honorifics
        # get all possible candidates
        candidates = itertools.product(*[
            pair2honorifics.get(pair, {pair, })
            for pair in self.out.split(SEP)
        ])
        # remove empty candidates
        candidates = [
            [pair.split(SEP) for pair in candidate if pair != NULL]
            for candidate in candidates
        ]
        # flatten pairs
        candidates = [
            list(itertools.chain(*candidate))
            for candidate in candidates
        ]
        # a list of candidates
        self.out = candidates
        return self

    @log
    def guess(self):
        """
        Guess the scores.
        """
        self.out: List[List[str]]
        politeness = self.logs['honorify']['in']['politeness']
        original_pairs = self.logs['analyze']['out'].split(SEP)
        if politeness == 0:
            boost_pairs = CASUAL & set(original_pairs)
        elif politeness == 1:
            boost_pairs = POLITE & set(original_pairs)
        elif politeness == 2:
            boost_pairs = FORMAL & set(original_pairs)
        else:
            raise ValueError(f"politeness should be one of (0, 1, 2), but got {politeness}")
        scores = [self.scorer(set(candidate), boost_pairs) for candidate in self.out]
        self.out = [(candidate, score) for candidate, score in zip(self.out, scores)]
        return self

    @log
    def conjugate(self):
        """
        Conjugate the guesses to get the final result.
        """
        self.out: List[Tuple[List[str], float]]
        best = max(self.out, key=lambda x: x[1])[0]
        self.out = self.kiwi.join([(pair.split(TAG)[0], pair.split(TAG)[1]) for pair in best])
        return self
