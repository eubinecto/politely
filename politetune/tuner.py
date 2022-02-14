import numpy as np
import pandas as pd
from typing import Optional, List, Tuple
from pandas.io.formats.style import Styler
from _kiwipiepy import Token
from politetune.fetchers import fetch_abbreviations, fetch_honorifics, fetch_rules
from kiwipiepy import Kiwi


class Tuner:
    """
    a politeness tuner.

    """
    ABBREVIATIONS: dict = fetch_abbreviations()
    HONORIFICS: dict = fetch_honorifics()
    RULES: dict = fetch_rules()

    def __init__(self):
        self.kiwi = Kiwi()
        self.polite: Optional[bool] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> dict:
        self.polite = self.RULES[listener][visibility]
        # preprocess the sentence
        tuned = sent + "." if not sent.endswith(".") else sent  # for accurate pos-tagging
        tuned = tuned.replace(" ", " " * 2)  # for accurate spacing
        # tokenize the sentence, and replace all the EFs with their honorifics
        tokens = self.kiwi.tokenize(tuned)
        texts = [
            self.HONORIFICS[f"{token.form}+{token.tag}"][self.polite]
            if f"{token.form}+{token.tag}" in self.HONORIFICS.keys()
            else token.form
            for token in tokens
        ]
        # restore spacings
        starts = np.array([token.start for token in tokens] + [0])
        lens = np.array([token.len for token in tokens] + [0])
        sums = np.array(starts) + np.array(lens)
        spacings = (starts[1:] - sums[:-1]) > 0
        tuned = "".join([
            text + " " if spacing else text
            for text, spacing in zip(texts, spacings)
        ])
        # abbreviate tokens
        for key, val in self.ABBREVIATIONS.items():
            tuned = tuned.replace(key, val)
        # post-process the sentence
        if not sent.endswith("."):
            tuned = tuned.replace(".", "")
        return {
            "tuned": tuned,
            "rules": self.highlight_rules(listener, visibility),
            "honorifics": self.highlight_honorifics(tokens)
        }

    def highlight_rules(self, listener: str, visibility: str) -> Styler:
        styler = pd.DataFrame(self.RULES).transpose().style
        subset = pd.IndexSlice[(listener, visibility)]
        styler = styler.applymap(lambda x: "background-color: purple", subset=subset)
        return styler

    def highlight_honorifics(self, tokens: Token) -> Styler:
        styler = pd.DataFrame(self.HONORIFICS).transpose().style
        for token in tokens:
            if f"{token.form}+{token.tag}" in self.HONORIFICS.keys():
                subset = pd.IndexSlice[(f"{token.form}+{token.tag}", self.polite)]
                styler = styler.applymap(lambda x: "background-color: purple", subset=subset)
        return styler
