from politetune.paths import ZULU_JVM, HONORIFICS_JSON, RULES_JSON
import pandas as pd


def fetch_honorifics() -> pd.DataFrame:
    return pd.read_json(str(HONORIFICS_JSON)).transpose()


def fetch_rules() -> pd.DataFrame:
    return pd.read_json(str(RULES_JSON)).transpose()
