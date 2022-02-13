from typing import Optional, List, Tuple
import pandas as pd
from pandas.io.formats.style import Styler
from politetune.fetchers import fetch_honorifics, fetch_rules
from kiwipiepy import Kiwi


class Honorifier:
    HONORIFICS: pd.DataFrame = fetch_honorifics()
    RULES: pd.DataFrame = fetch_rules()

    def __init__(self):
        self.kiwi = Kiwi()
        self.honored: Optional[bool] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> Tuple[str, Styler, Styler]:
        self.honored = self.RULES.loc[listener][visibility]
        for lemma, (token, pos) in zip(lemmas, tok2pos):
            if lemma in self.HONORIFICS.index and pos == self.HONORIFICS.loc[lemma]['pos']:
                sent = sent.replace(token, f"`{self.HONORIFICS.loc[lemma][self.honored]}`")
        return sent, self.highlight_rules(listener, visibility), self.highlight_honorifics(lemmas, tok2pos)

    def highlight_rules(self, listener: str, visibility: str) -> Styler:
        subset = pd.IndexSlice[(listener, visibility)]
        styler = self.RULES.style.applymap(lambda x: "background-color: purple", subset=subset)
        return styler

    def highlight_honorifics(self, lemmas: List[str], tok2pos: List[Tuple[str, str]]) -> Styler:
        styler = self.HONORIFICS.style
        for lemma, (token, pos) in zip(lemmas, tok2pos):
            if lemma in self.HONORIFICS.index and pos == self.HONORIFICS.loc[lemma]['pos']:
                subset = pd.IndexSlice[(lemma, self.honored)]
                styler = styler.applymap(lambda x: "background-color: purple", subset=subset)
        return styler

