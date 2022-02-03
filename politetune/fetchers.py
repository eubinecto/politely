import platform
from typing import List
from konlpy.tag import Okt
from politetune.paths import ZULU_JVM, HONORIFICS_YAML, RULES_YAML, VISIBILITIES_YAML
import json
import pandas as pd


def fetch_honorifics() -> pd.DataFrame:
    return pd.read_json(str(HONORIFICS_YAML)).transpose()


def fetch_rules() -> pd.DataFrame:
    return pd.read_json(str(RULES_YAML)).transpose()


def fetch_visibilities() -> List[str]:
    with open(str(VISIBILITIES_YAML), "r") as fh:
        return json.load(fh)


def fetch_okt() -> Okt:
    if platform.processor() == "arm":
        return Okt(jvmpath=str(ZULU_JVM))  # fetch okt with m1-compatible jvm
    else:
        return Okt()
