import os
from politely.fetchers import fetch_honorifics

DLM = "⊕"
SEP = "⎸"
os.environ["DLM"] = DLM
os.environ["SEP"] = SEP
HONORIFICS = fetch_honorifics()

from politely.styler import Styler  # noqa

__version__ = "v3.1.1"
