from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = LIB_DIR / "resources"

# files
HONORIFICS_YAML = RESOURCES_DIR / "honorifics.json"
RULES_YAML = RESOURCES_DIR / "rules.json"
VISIBILITIES_YAML = RESOURCES_DIR / "visibilities.json"


ZULU_JVM = Path("/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java")
