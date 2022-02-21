
import numpy as np
import pandas as pd
from kiwipiepy import Kiwi
from pandas.io.formats.style import Styler
from typing import Optional, List, Tuple
from politetune.fetchers import fetch_abbreviations, fetch_honorifics, fetch_rules


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
        self.rule: Optional[Tuple[str, str]] = None
        self.honorifics: Optional[List[Tuple[str, str]]] = None
        self.abbreviations: Optional[List[Tuple[str, str]]] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> str:
        # preprocess the sentence
        preprocessed = sent + "." if not sent.endswith(".") else sent  # for accurate pos-tagging
        preprocessed = preprocessed.replace(" ", " " * 2)  # for accurate spacing
        # tokenize the sentence, and replace all the EFs with their honorifics
        tokens = self.kiwi.tokenize(preprocessed)
        polite = self.RULES[listener][visibility]
        texts = [
            self.HONORIFICS[f"{token.form}+{token.tag}"][polite]
            if f"{token.form}+{token.tag}" in self.HONORIFICS.keys()
            else token.form
            for token in tokens
        ]
        # restore spacings
        starts = np.array([token.start for token in tokens] + [0])
        lens = np.array([token.len for token in tokens] + [0])
        sums = np.array(starts) + np.array(lens)
        spacings = (starts[1:] - sums[:-1]) > 0
        spaced = "".join([
            text + " " if spacing else text
            for text, spacing in zip(texts, spacings)
        ])
        # abbreviate tokens
        abbreviated = spaced
        for key, val in self.ABBREVIATIONS.items():
            abbreviated = abbreviated.replace(key, val)
        # post-process the sentence
        tuned = abbreviated
        if not sent.endswith("."):
            tuned = tuned.replace(".", "")
        # register any information to be used for post-processing
        self.polite = polite
        self.rule = (listener, visibility)
        self.honorifics = [
            (f"{token.form}+{token.tag}", polite)
            for token in tokens
            if f"{token.form}+{token.tag}" in self.HONORIFICS.keys()
        ]
        self.abbreviations = [
            (key, "abbreviation")
            for key, val in self.ABBREVIATIONS.items()
            if key in spaced
        ]
        return tuned


class Highlighter:
    """
    This should work independent of Tuner.
    """
    ABBREVIATIONS: pd.DataFrame = pd.DataFrame.from_dict(fetch_abbreviations(), orient="index",
                                                         columns=["abbreviation"])
    RULES: pd.DataFrame = pd.DataFrame(fetch_rules()).transpose()
    HONORIFICS: pd.DataFrame = pd.DataFrame(fetch_honorifics()).transpose()

    def __call__(self, rule: Tuple[str, str], honorifics: List[Tuple[str, str]],
                 abbreviations: List[Tuple[str, str]]) -> Tuple[Styler, Styler, Styler]:
        """
        :param rule: The rule applied
        :param honorifics: The honorifics applied
        :return: Two stylers
        """
        styler_rule = self.highlight_rule(rule)
        styler_honorifics = self.highlight_honorifics(honorifics)
        styler_abbreviations = self.highlight_abbreviations(abbreviations)
        return styler_rule, styler_honorifics, styler_abbreviations

    def highlight_rule(self, rule: Tuple[str, str]) -> Styler:
        styler = self.RULES.style
        styler = styler.applymap(lambda x: "background-color: purple", subset=rule)
        return styler

    def highlight_honorifics(self, honorifics: List[Tuple[str, str]]) -> Styler:
        styler = self.HONORIFICS.style
        for honorific in honorifics:
            styler = styler.applymap(lambda x: "background-color: purple", subset=honorific)
        return styler

    def highlight_abbreviations(self, abbreviations: List[Tuple[str, str]]) -> Styler:
        styler = self.ABBREVIATIONS.style
        for abbreviated in abbreviations:
            styler = styler.applymap(lambda x: "background-color: purple", subset=abbreviated)
        return styler

    @property
    def listeners(self):
        return self.RULES.index

    @property
    def visibilities(self):
        return self.RULES.columns
