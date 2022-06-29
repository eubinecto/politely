from politely.fetchers import fetch_rules, fetch_honorifics, fetch_listeners, fetch_environs

# initialise the constants globally here
RULES = fetch_rules()
HONORIFICS = fetch_honorifics()
LISTENERS = fetch_listeners()
ENVIRONS = fetch_environs()

# quick access
from politely.styler import Styler


__version__ = "v3.0.0"
