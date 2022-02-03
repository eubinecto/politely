from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = LIB_DIR / "resources"

# files
HONORIFICS_JSON = RESOURCES_DIR / "honorifics.json"
RULES_JSON = RESOURCES_DIR / "rules.json"


ZULU_JVM = Path("/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java")
