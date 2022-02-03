import platform
from typing import List
from konlpy.tag import Okt
from politetune.paths import ZULU_JVM, HONORIFICS_YAML, RULES_YAML, VISIBILITIES_YAML
import yaml


def fetch_honorifics() -> dict:
    with open(str(HONORIFICS_YAML), "r") as fh:
        return yaml.safe_load(fh)


def fetch_rules() -> dict:
    with open(str(RULES_YAML), "r") as fh:
        return yaml.safe_load(fh)


def fetch_visibilities() -> List[str]:
    with open(str(VISIBILITIES_YAML), "r") as fh:
        return yaml.safe_load(fh)


def fetch_okt() -> Okt:
    if platform.processor() == "arm":
        return Okt(jvmpath=str(ZULU_JVM))  # fetch okt with m1-compatible jvm
    else:
        return Okt()
