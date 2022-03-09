
import pandas as pd
from khaiii.khaiii import KhaiiiApi
from typing import Optional
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
        self.polite: Optional[bool] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> str:
        # append a period if it is not appended
        tuned = sent + "." if not sent.endswith(".") else sent  # for accurate pos-tagging
        # tokenize the sentence, and replace all the EFs with their honorifics
        polite = self.RULES[listener][visibility]
        tokens = self.khaiii.analyze(tuned)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        tuned = " ".join([
            "".join([
                self.HONORIFICS[morph][polite] if morph in self.HONORIFICS
                else morph.split("/")[0]
                for morph in morphs
            ])
            if set(morphs) & set(self.HONORIFICS.keys()) else lex
            for lex, morphs in lexicon2morphs
        ])
        # abbreviate tokens
        for key, val in self.ABBREVIATIONS.items():
            tuned = tuned.replace(key, val)
        # apply irregular rules
        for key, val in self.IRREGULARS.items():
            tuned = tuned.replace(key, val)
        # remove or leave the period
        tuned = tuned.replace(".", "") if not sent.endswith(".") else tuned
        # register any information to be used for post-processing
        self.polite = polite
        self.rule = (listener, visibility)
        return tuned

    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def visibilities(self):
        return pd.DataFrame(self.RULES).transpose().columns
