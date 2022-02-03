from typing import Optional, List, Tuple
from politetune.fetchers import fetch_okt, fetch_honorifics, fetch_rules, fetch_visibilities


class Honorifier:

    def __init__(self):
        self.okt = fetch_okt()
        self.honorifics = fetch_honorifics()
        self.rules = fetch_rules()
        self.visibilities = fetch_visibilities()
        self.honored: Optional[bool] = None

    def __call__(self, sent: str, listener: str, visibility: str) -> str:
        self.honored = self.rules[listener][visibility]
        lemmas: List[str] = self.okt.morphs(sent, stem=True)
        tok2pos: List[Tuple[str, str]] = self.okt.pos(sent)
        for lemma, (token, pos) in zip(lemmas, tok2pos):
            if lemma in self.honorifics and pos == self.honorifics[lemma]['pos']:
                sent = sent.replace(token, f"`{self.honorifics[lemma][self.honored]}({pos})`")
        return sent
