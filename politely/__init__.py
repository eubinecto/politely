import os
from politely.fetchers import fetch_honorifics

DEL = "⊕"
SEP = "⵰"
os.environ["DEL"] = DEL
os.environ["SEP"] = SEP
HONORIFICS = fetch_honorifics()

from politely.styler import Styler  # noqa

__version__ = "v3.1.0"
