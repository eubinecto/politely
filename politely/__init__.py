from politely.fetchers import fetch_rules, fetch_honorifics
from politely.stylers import styler
from khaiii.khaiii import KhaiiiApi
import pandas as pd  # noqa

# initialise the resources to use
RULES = fetch_rules()
HONORIFICS = fetch_honorifics()
LISTENERS = pd.DataFrame(RULES).transpose().index
ENVIRONS = pd.DataFrame(RULES).transpose().columns
# initialise the analyser to use
analyser = KhaiiiApi()
