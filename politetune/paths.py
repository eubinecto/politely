from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = LIB_DIR / "resources"

# files
ABBREVIATIONS_JSON = RESOURCES_DIR / "abbreviations.json"
HONORIFICS_JSON = RESOURCES_DIR / "honorifics.json"
RULES_JSON = RESOURCES_DIR / "rules.json"
