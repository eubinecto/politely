from politely.fetchers import fetch_rules, fetch_honorifics, fetch_listeners, fetch_environs
import pandas as pd  # noqa

# initialise the global constants here
RULES = fetch_rules()
HONORIFICS = fetch_honorifics()
LISTENERS = fetch_listeners()
ENVIRONS = fetch_environs()

# quick access
from politely.stylers import style
