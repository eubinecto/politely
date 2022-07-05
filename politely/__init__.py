import os
from politely.fetchers import fetch_honorifics

DEL = "⊕"
os.environ["DEL"] = DEL
HONORIFICS = fetch_honorifics()

from politely.styler import Styler  # noqa

__version__ = "v3.0.0"
