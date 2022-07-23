from typing import List
from politely import TAG


class Scorer:
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
