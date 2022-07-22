from politely import TAG


class Scorer:
    def __call__(self, morph: str) -> float:
        """
        Very rudimentary scoring function. Does not regard the context at all.
        Perhaps turn this into a Scorer class, in case you get to use a language model.
        """
        if morph in (f"어{TAG}EF",
                     f"어요{TAG}EF",
                     f"어요{TAG}EF",
                     f"습니다{TAG}EF",
                     f"ᆸ니다{TAG}EF"):
            return 1
        else:
            return 0
