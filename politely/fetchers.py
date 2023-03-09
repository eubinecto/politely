from kiwipiepy import Kiwi
from politely.scorer import Scorer


def fetch_scorer() -> Scorer:
    """
    use fetch_scorer to
    """
    # as of right now, Scorer is not really "fetched".
    # we define this function nevertheless, as  we will need this by the time
    # we use n-grams for the scorer.
    return Scorer()


def fetch_kiwi() -> Kiwi:
    """
    fetch kiwi with user-defined rules
    """
    kiwi = Kiwi()
    kiwi.add_user_word(".", tag="SF")
    kiwi.add_user_word("우리말", tag="NNP", score=1)
    kiwi.add_pre_analyzed_word(
        "벗어.", [("벗", "VV-R"), ("어", "EF"), (".", "SF")], score=1
    )
    return kiwi
