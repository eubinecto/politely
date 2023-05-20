from typing import List


class Scorer:

    def __call__(self,  candidates: List[List[str]], *args, **kwargs) -> List[float]:
        raise NotImplementedError
