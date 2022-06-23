import oyaml as yaml
import pandas as pd  # noqa
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
