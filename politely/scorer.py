from typing import Set
from politely import PREFERENCES


class Scorer:

    def __call__(self, pairs: Set[str], boost_pairs: Set[str]) -> float:
        """
        A naive scoring function.
        """
        # if it includes priority pairs, it's a good candidate (at least for this scorer)
        score = (len(PREFERENCES & pairs) / len(pairs)) * 0.1
        score += (len(boost_pairs & pairs) / len(pairs)) * 0.9
        return score
