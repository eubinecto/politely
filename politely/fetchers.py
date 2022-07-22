import os
from pathlib import Path
from kiwipiepy import Kiwi
import oyaml


def fetch_honorifics() -> dict:
    with open(Path(__file__).resolve().parent / "honorifics.yaml", "r") as f:
        honorifics = oyaml.safe_load(os.path.expandvars(f.read()))
    return honorifics


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
