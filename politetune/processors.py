
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
        self.honorifics: List[Tuple[str, str]] = list()
        self.abbreviations: List[Tuple[str, str]] = list()

    def __call__(self, sent: str, listener: str, visibility: str) -> str:
        # preprocess the sentence
        tuned = sent + "." if not sent.endswith(".") else sent  # for accurate pos-tagging
        # tokenize the sentence, and replace all the EFs with their honorifics
        tokens = self.kiwi.tokenize(tuned)
        polite = self.RULES[listener][visibility]
        # honorify tokens
        for token in tokens:
            key = f"{token.form}+{token.tag}"
            if key in self.HONORIFICS.keys():
                honorific = self.HONORIFICS[key][polite]
                # TODO: 무작정 교체만 하고 있을수는 없다...는 것이 문제다...
                tuned = tuned[:token.start] + honorific + tuned[token.end:]
                self.honorifics.append((key, polite))  # need this for highlighting
        # abbreviate tokens
        for key, val in self.ABBREVIATIONS.items():
            tuned = tuned.replace(key, val)
            self.abbreviations.append((key, "abbreviation"))
        # post-process the sentence
        if not sent.endswith("."):
            tuned = tuned.replace(".", "")
        # register any information to be used for post-processing
        self.polite = polite
        self.rule = (listener, visibility)
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
