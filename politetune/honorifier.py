from typing import Optional, List, Tuple
import pandas as pd
from pandas.io.formats.style import Styler
from politetune.fetchers import fetch_okt, fetch_honorifics, fetch_rules, fetch_visibilities


class Honorifier:
    HONORIFICS: pd.DataFrame = fetch_honorifics()
    RULES: pd.DataFrame = fetch_rules()
    VISIBILITIES: List[str] = fetch_visibilities()

    def __init__(self):
        self.okt = fetch_okt()
        self.honored: Optional[bool] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> Tuple[str, Styler, Styler]:
        self.honored = self.RULES.loc[listener][visibility]
        lemmas: List[str] = self.okt.morphs(sent, stem=True)
        tok2pos: List[Tuple[str, str]] = self.okt.pos(sent)
        for lemma, (token, pos) in zip(lemmas, tok2pos):
            if lemma in self.HONORIFICS.index and pos == self.HONORIFICS.loc[lemma]['pos']:
                sent = sent.replace(token, f"`{self.HONORIFICS.loc[lemma][self.honored]}({pos})`")
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

