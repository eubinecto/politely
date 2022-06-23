"""
A script for styling it.
"""

import re
from typing import Tuple
import requests  # noqa
import pandas as pd  # noqa
from politely.errors import EFNotIncludedError, EFNotSupportedError
from politely import RULES, HONORIFICS
from politely.hangle import conjugate as politely_conjugate
from multipledispatch import dispatch
from functools import wraps
from khaiii.khaiii import KhaiiiApi

# to be used within functions
analyser = KhaiiiApi()


# --- decorators --- #
def _log(f):
    """
    log the in's and out's of the function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        # TODO: log the in's and out's
        return out

    return wrapper


def _preprocess(sent: str) -> str:
    out = sent.strip()  # khaiii model is sensitive to empty spaces, so we should get rid of it.
    if not out.endswith("?") and not out.endswith("!"):
        out = out + "." if not out.endswith(".") else out  # for accurate pos-tagging
    return out


def _matched(pattern: str, string: str) -> bool:
    return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False


def _check(tokens: list) -> list:
    """
    Check if your assumption holds. Raises a custom error if any of them does not hold.
    """
    efs = ["+".join(map(str, token.morphs)) for token in tokens if "EF" in "+".join(map(str, token.morphs))]
    # assumption 1: the sentence must include more than 1 EF's
    if not efs:
        raise EFNotIncludedError("|".join(["+".join(map(str, token.morphs)) for token in tokens]))
    # assumption 2: all EF's should be supported by KPS.
    for ef in efs:
        for pattern in HONORIFICS.keys():
            if _matched(pattern, ef):
                break
        else:
            raise EFNotSupportedError(ef)
    return tokens


@_log
def _analyze(sent: str) -> list:
    return analyser.analyze(sent)


@_log
def _honorify(tokens: list, politeness: int) -> list:
    lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
    out = list()
    for lex, morphs in lex2morphs:
        tuned = "+".join(morphs)
        for pattern in HONORIFICS.keys():
            if _matched(pattern, tuned):
                honorific = HONORIFICS[pattern][politeness]
                tuned = tuned.replace(pattern, honorific)
                # TODO: log the honorifics here
        # if something has changed, then go for it, but otherwise just use the lex.
        before = [morph.split("/")[0] for morph in morphs]
        after = [morph.split("/")[0] for morph in tuned.split("+")]
        if "".join(before) != "".join(after):
            out.append(after)
        else:
            out.append(lex)
    return out


@_log
def _conjugate(tokens: list) -> str:
    """
    Progressively conjugate morphemes from left to right.
    """
    out = list()
    for chunk in tokens:
        if not isinstance(chunk, list):
            out.append(chunk)
        else:
            left = chunk[0]
            for i in range(len(chunk) - 1):
                right = chunk[i + 1]
                left = politely_conjugate(left, right)
            out.append(left)
    return " ".join(out)


# --- stylers --- #
@dispatch(str, int)
def style(sent: str, politeness: int) -> Tuple[str, dict]:
    """
    The first way of using style.
    """
    out = _preprocess(sent)
    out = _analyze(out)
    out = _check(out)
    out = _honorify(out, politeness)
    out = _conjugate(out)
    # TODO: collect all the logs here
    logs = ...
    return out, logs


@dispatch(str, str, str)
def style(sent: str, listener: str, environ: str) -> Tuple[str, dict]:
    """
    The second way of using style.
    """
    case = RULES[listener][environ]
    out, logs = style(sent, case["politeness"])
    logs.update(...)
    return out, logs
