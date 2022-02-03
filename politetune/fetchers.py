import platform
from konlpy.tag import Okt, Komoran
from politetune.paths import ZULU_JVM, HONORIFICS_JSON, RULES_JSON
import pandas as pd


def fetch_honorifics() -> pd.DataFrame:
    return pd.read_json(str(HONORIFICS_JSON)).transpose()


def fetch_rules() -> pd.DataFrame:
    return pd.read_json(str(RULES_JSON)).transpose()


def fetch_okt() -> Okt:
    if platform.processor() == "arm":
        return Okt(jvmpath=str(ZULU_JVM))  # fetch okt with m1-compatible jvm
    else:
        return Okt()


def fetch_komoran() -> Komoran:
    if platform.processor() == "arm":
        return Komoran(jvmpath=str(ZULU_JVM))  # fetch okt with m1-compatible jvm
    else:
        return Komoran()