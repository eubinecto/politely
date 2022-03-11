
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
        self.out: Any = None
        self.listener: Optional[str] = None
        self.visibility: Optional[str] = None

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
        self.out = self.out.replace("전", "저는")\
                           .replace("넌", "너는")\
                           .replace("난", "나는")

    def apply_honorifics(self):
        polite = self.RULES[self.listener][self.visibility]
        tokens = self.khaiii.analyze(self.out)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        self.out = " ".join([
            "".join([
                self.HONORIFICS[morph][polite] if morph in self.HONORIFICS
                else morph.split("/")[0]
                for morph in morphs
            ])
            if set(morphs) & set(self.HONORIFICS.keys()) else lex
            for lex, morphs in lexicon2morphs
        ])

    def apply_abbreviations(self):
        for key, val in self.ABBREVIATIONS.items():
            self.out = self.out.replace(key, val)

    def apply_irregulars(self):
        for key, val in self.IRREGULARS.items():
            self.out = self.out.replace(key, val)

    def postprocess(self):
        self.out = self.out.replace(".", "") if not self.sent.endswith(".") else self.out

    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def visibilities(self):
        return pd.DataFrame(self.RULES).transpose().columns
