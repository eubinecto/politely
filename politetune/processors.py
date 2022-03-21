import itertools

import pandas as pd
from khaiii.khaiii import KhaiiiApi
from typing import Optional, Any, Callable, List
from politetune.fetchers import fetch_abbreviations, fetch_honorifics, fetch_rules, fetch_irregulars


class Tuner:
    """
    a politeness tuner.
    """
    ABBREVIATIONS: dict = fetch_abbreviations()
    HONORIFICS: dict = fetch_honorifics()
    RULES: dict = fetch_rules()
    IRREGULARS: dict = fetch_irregulars()

    def __init__(self):
        self.khaiii = KhaiiiApi()
        # inputs
        self.sent: Optional[str] = None
        self.listener: Optional[str] = None
        self.visibility: Optional[str] = None
        # the output can be anything
        self.out: Any = None

    def __call__(self, sent: str, listener: str, visibility: str) -> str:
        # register inputs
        self.sent = sent
        self.listener = listener
        self.visibility = visibility
        # process each step
        for step in self.steps():
            step()
        # return the final output
        return self.out

    def steps(self) -> List[Callable]:
        return [
            self.preprocess,
            self.apply_honorifics,
            self.apply_abbreviations,
            self.apply_irregulars,
            self.postprocess
        ]

    def preprocess(self):
        self.out = self.sent + "." if not self.sent.endswith(".") else self.sent  # for accurate pos-tagging

    def apply_honorifics(self):
        polite = self.RULES[self.listener][self.visibility]
        tokens = self.khaiii.analyze(self.out)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        out = list()
        for lex, morphs in lexicon2morphs:
            # this is to be used just for matching
            substrings = ["+".join(morphs[i:j]) for i, j in itertools.combinations(range(len(morphs) + 1), 2)]
            if set(substrings) & set(self.HONORIFICS.keys()):  # need to make sure any patterns match joined.
                tuned = "+".join(morphs)
                for pattern in self.HONORIFICS.keys():
                    tuned = tuned.replace(pattern, self.HONORIFICS[pattern][polite])
                tuned = "".join([token.split("/")[0] for token in tuned.split("+")])
                out.append(tuned)
            else:
                out.append(lex)
        self.out = " ".join(out)

    def apply_abbreviations(self):
        for key, val in self.ABBREVIATIONS.items():
            self.out = self.out.replace(key, val)

    def apply_irregulars(self):
        for key, val in self.IRREGULARS.items():
            self.out = self.out.replace(key, val)

    def postprocess(self):
        self.out = self.out[:-1] if not self.sent.endswith(".") else self.out

    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def visibilities(self):
        return pd.DataFrame(self.RULES).transpose().columns


class Explainer:
    """
    This is here to explain each step in tuner.
    """
    pass

