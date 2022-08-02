from pathlib import Path
from typing import List
from gensim.models import Word2Vec
from politely import TAG


class Scorer:

    def __init__(self):
        # I just want to experiment with this.
        # self.w2v = Word2Vec.load(str(Path(__file__).resolve().parent.parent / "stylekqc.w2v"))
        # TODO: experiment with word2vec, or a language model.
        pass

    def __call__(self, tokens: List[str]) -> float:
        """
        Very rudimentary scoring function. Does not regard the context at all.
        Perhaps turn this into a Scorer class, in case you get to use a language model.
        """
        priorities = (f"어{TAG}EF",
                      f"어요{TAG}EF",
                      f"어요{TAG}EF",
                      f"습니다{TAG}EF",
                      f"ᆸ니다{TAG}EF")
        if any([priority in tokens for priority in priorities]):
            return 1
        else:
            return 0
