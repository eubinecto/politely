"""
What you needed was itertools.product()!
https://www.adamsmith.haus/python/answers/how-to-get-all-unique-combinations-of-two-lists-in-python
bingo! This is exactly what I wanted.
"""

import itertools
from pprint import pprint

sent = ["e", 'f', "a", "d", "b", "c", "g"]

candidates = {
    "a": {"hi", "hello", "bye"},
    "b": {"there", "here", "now"},
    "c": {"you", "me", "us"}
}
sent = [
    candidates.get(token, token)
    for token in sent
]
products = itertools.product(*sent)
pprint(list(products))
