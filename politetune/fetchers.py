import json
from politetune.paths import HONORIFICS_JSON, RULES_JSON, ABBREVIATIONS_JSON


def fetch_abbreviations() -> dict:
    with open(str(ABBREVIATIONS_JSON), 'r') as fh:
        return json.loads(fh.read())


def fetch_honorifics() -> dict:
    with open(str(HONORIFICS_JSON), 'r') as fh:
        return json.loads(fh.read())


def fetch_rules() -> dict:
    with open(str(RULES_JSON), 'r') as fh:
        return json.loads(fh.read())

