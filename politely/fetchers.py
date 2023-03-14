from kiwipiepy import Kiwi


def fetch_kiwi() -> Kiwi:
    """
    fetch kiwi with user-defined rules
    """
    kiwi = Kiwi()
    kiwi.add_user_word(".", tag="SF")
    kiwi.add_user_word("우리말", tag="NNP", score=1)
    kiwi.add_user_word("점순이", tag="NNP", score=1)
    kiwi.add_user_word("란다", tag="EF", score=1)
    kiwi.add_user_word("래요", tag="EF", score=1)
    kiwi.add_user_word("랍니다", tag="EF", score=1)
    kiwi.add_pre_analyzed_word(
        "벗어.", [("벗", "VV-R"), ("어", "EF"), (".", "SF")], score=1
    )
    return kiwi
