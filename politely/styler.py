import itertools
import os
import re
from copy import copy, deepcopy
import random
from typing import Any, List, Tuple, Dict, Set
from functools import wraps
import numpy as np
import torch
from politely.errors import EFNotSupportedError, SFNotIncludedError, EFNotIncludedError
from politely.fetchers import fetch_kiwi
from politely import RULES, SEP, TAG, NULL, SELF
from politely.modeling_gpt2_scorer import GPT2Scorer
from politely.modeling_scorer import Scorer
from politely.rules import EFS


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
    def __init__(self, strict: bool = False, scorer: Scorer = GPT2Scorer()):
        #  --- object-owned attributes --- #
        self.scorer = scorer
        self.strict = strict
        self.out: Any = None
        self.kiwi = fetch_kiwi()
        self.rules = deepcopy(RULES)
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
        # --- seed everything --- #
        seed = 318
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True
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
            # assumption 2: every sentence should include a valid EF. It should match the EFS pattern.
            if "EF" not in self.out:
                raise EFNotIncludedError(self.out)
            # assumption 3: all EF's should be supported by politely.
            if not all([re.match(EFS, pair) for pair in self.out.split(SEP) if "EF" in pair]):
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
        for pattern in self.rules.keys():
            match = re.search(pattern, self.out)
            if match:
                # should be only one pair
                pair = match.group("MASK")
                honorifics = {honorific.replace(SELF, pair) for honorific in self.rules[pattern][politeness]}
                # progressively narrow down honorifics
                pair2honorifics[pair] = pair2honorifics.get(pair, honorifics) & honorifics
        # get all possible candidates
        candidates = itertools.product(*[
            pair2honorifics.get(pair, {pair, })
            for pair in self.out.split(SEP)  # SEP
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
        # score each candidate
        scores = self.scorer(self.out, self.logs, self.kiwi)
        self.out = [(candidate, score) for candidate, score in zip(self.out, scores)]
        return self

    def conjugate(self):
        """
        Elect the best candidate and conjugate its pairs.
        """
        self.out: List[Tuple[List[str], float]]
        best = max(self.out, key=lambda x: x[1])[0]
        self.out = self.kiwi.join([(pair.split(TAG)[0], pair.split(TAG)[1]) for pair in best])
        return self

    def add_rules(self, rules: Dict[str, Tuple[Set,
                                               Set,
                                               Set]]):
        """
        Add rules to the existing rules.
        """
        # check if the rules are in proper format
        for key, _ in rules.items():
            # first, check if the key includes a group with the key; (?<MASK>...)
            # e.g. (?P<MASK>(아빠|아버지){TAG}NNG)
            if not re.search(re.escape(r"(?P<MASK>") + r".*" + re.escape(")"), key):
                raise ValueError(f"key should include a group with the key; (?P<MASK>...), but got {key}")
        self.rules.update(rules)
        return self
        