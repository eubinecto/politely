import oyaml as yaml
import pandas as pd  # noqa
from kiwipiepy import Kiwi

from politely.paths import HONORIFICS_YAML, RULES_YAML


def fetch_honorifics() -> dict:
    with open(str(HONORIFICS_YAML), "r") as fh:
        return yaml.safe_load(fh)


def fetch_rules() -> dict:
    with open(str(RULES_YAML), "r") as fh:
        return yaml.safe_load(fh)


def fetch_listeners() -> list:
    rules = fetch_rules()
    return pd.DataFrame(rules).transpose().index.tolist()


def fetch_environs() -> list:
    rules = fetch_rules()
    return pd.DataFrame(rules).transpose().columns.tolist()


def fetch_kiwi() -> Kiwi:
    kiwi = Kiwi()
    kiwi.add_user_word(".", tag="SF")
    kiwi.add_pre_analyzed_word("벗어.", [('벗', 'VV-R'), ('어', 'EF'), ('.', 'SF')], score=1)
    return kiwi
