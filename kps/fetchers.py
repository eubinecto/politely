import oyaml as yaml
from kps.paths import HONORIFICS_YAML, RULES_YAML, ABBREVIATIONS_YAML, IRREGULARS_YAML


def fetch_abbreviations() -> dict:
    with open(str(ABBREVIATIONS_YAML), 'r') as fh:
        return yaml.safe_load(fh)


def fetch_honorifics() -> dict:
    with open(str(HONORIFICS_YAML), 'r') as fh:
        return yaml.safe_load(fh)


def fetch_rules() -> dict:
    with open(str(RULES_YAML), 'r') as fh:
        return yaml.safe_load(fh)


def fetch_irregulars() -> dict:
    with open(str(IRREGULARS_YAML), 'r') as fh:
        return yaml.safe_load(fh)
