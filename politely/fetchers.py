import oyaml as yaml
from politely.paths import HONORIFICS_YAML, RULES_YAML


def fetch_honorifics() -> dict:
    with open(str(HONORIFICS_YAML), 'r') as fh:
        return yaml.safe_load(fh)


def fetch_rules() -> dict:
    with open(str(RULES_YAML), 'r') as fh:
        return yaml.safe_load(fh)
