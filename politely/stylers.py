import inspect
import re
import requests  # noqa
import pandas as pd  # noqa
from politely.errors import EFNotIncludedError, EFNotSupportedError
from politely import analyser, RULES, HONORIFICS
from politely.hangle import conjugate as politely_conjugate
from multipledispatch import dispatch
from functools import wraps


# --- decorators --- #
def log(f):
    """
    log the in's and out's of the function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        # TODO: log the in's and out's
        return out
    return wrapper


def preprocess(sent: str) -> str:
    out = sent.strip()  # khaiii model is sensitive to empty spaces, so we should get rid of it.
    if not out.endswith("?") and not out.endswith("!"):
        out = out + "." if not out.endswith(".") else out  # for accurate pos-tagging
    return out


def matched(pattern: str, string: str) -> bool:
    return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False


def check(tokens: list) -> list:
    """
    Check if your assumption holds. Raises a custom error if any of them does not hold.
    """
    efs = [
        "+".join(map(str, token.morphs)) for token in tokens if "EF" in "+".join(map(str, token.morphs))
    ]
    # assumption 1: the sentence must include more than 1 EF's
    if not efs:
        raise EFNotIncludedError("|".join(["+".join(map(str, token.morphs)) for token in tokens]))
    # assumption 2: all EF's should be supported by KPS.
    for ef in efs:
        for pattern in HONORIFICS.keys():
            if matched(pattern, ef):
                break
        else:
            raise EFNotSupportedError(ef)
    return tokens


@log
def analyze(sent: str) -> list:
    return analyser.analyze(sent)


@log
def honorify(tokens: list, politeness: int) -> list:
    lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
    out = list()
    for lex, morphs in lex2morphs:
        tuned = "+".join(morphs)
        for pattern in HONORIFICS.keys():
            if matched(pattern, tuned):
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


@log
def conjugate(tokens: list) -> str:
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


@dispatch(str, str, str)
def style(sent: str, listener: str, environ: str) -> str:
    case = RULES[listener][environ]
    # TODO: log the case
    out = preprocess(sent)
    out = analyze(out)
    out = check(out)
    out = honorify(out, case['politeness'])
    out = conjugate(out)
    return out


@dispatch(str, int)
def style(sent: str, politeness: int) -> str:
    out = preprocess(sent)
    out = analyze(out)
    out = check(out)
    out = honorify(out, politeness)
    out = conjugate(out)
    return out

