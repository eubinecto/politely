import inspect
import os
import re
import requests  # noqa
import pandas as pd  # noqa
import streamlit as st
from khaiii.khaiii import KhaiiiApi
from typing import Any, Tuple, Set
from politely.fetchers import fetch_abbreviations, fetch_honorifics, fetch_rules, fetch_irregulars
from politely.errors import EFNotIncludedError, EFNotSupportedError
from multipledispatch import dispatch
from dataclasses import dataclass, field


class Styler:
    """
    A rule-based Korean Politeness Styler
    """
    @dataclass
    class Logs:
        args: dict = field(default_factory=dict)
        case: dict = field(default_factory=dict)
        steps: list = field(default_factory=list)
        conjugations: Set[Tuple[str, str]] = field(default_factory=set)
        abbreviations: Set[Tuple[str, str]] = field(default_factory=set)
        irregulars: Set[Tuple[str, str]] = field(default_factory=set)
    # class-owned attributes
    RULES: dict = fetch_rules()
    HONORIFICS: dict = fetch_honorifics()
    ABBREVIATIONS: dict = fetch_abbreviations()
    IRREGULARS: dict = fetch_irregulars()

    def __init__(self):
        # object-owned attributes
        self.khaiii = KhaiiiApi()
        self.out: Any = None
        self.logs = self.Logs()

    @dispatch(str, str, str)
    def __call__(self, sent: str, listener: str, environ: str) -> str:
        """
        First way of using Styler - have Styler determine the politeness for you.
        """
        self.clear() \
            .save() \
            .determine(listener, environ) \
            .process(sent, self.logs.case['politeness'])
        return self.out

    @dispatch(str, int)
    def __call__(self, sent: str, politeness: int) -> str:
        """
        The other way of using Styler - you know your politeness already, just use this as a styler per se.
        This would more suitable than the first __call__ for  e.g. augmentation of data purposes.
        """
        self.clear() \
            .save() \
            .process(sent, politeness)
        return self.out

    def process(self, sent: str, politeness: int):
        """
        The common steps for all __call__'s.
        """
        self.preprocess(sent) \
            .analyze() \
            .check() \
            .log() \
            .conjugate(politeness) \
            .log() \
            .abbreviate() \
            .log() \
            .irregulars() \
            .log()
        return self

    def save(self):
        """
        save whatever arguments that were provided to __call__
        """
        f_back = inspect.currentframe().f_back
        args = inspect.getargvalues(f_back)
        self.logs.args.update(args.locals)
        return self

    def clear(self):
        """
        clear all logs
        """
        self.logs.args.clear()
        self.logs.steps.clear()
        self.logs.conjugations.clear()
        self.logs.abbreviations.clear()
        self.logs.irregulars.clear()
        return self

    def log(self):
        """
        log the current out
        """
        self.logs.steps.append(self.out)
        return self

    def determine(self, listener: str, environ: str):
        """
        determine the case from the rules.
        """
        self.logs.case = self.RULES[listener][environ]
        return self

    def preprocess(self, sent: str):
        self.out = sent.strip()  # khaiii model is sensitive to empty spaces, so we should get rid of it.
        if not self.out.endswith("?") and not self.out.endswith("!"):
            self.out = self.out + "." if not self.out.endswith(".") else self.out  # for accurate pos-tagging
        return self

    def analyze(self):
        tokens = self.khaiii.analyze(self.out)
        self.out = tokens
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        efs = [
            "+".join(map(str, token.morphs))
            for token in self.out
            if "EF" in "+".join(map(str, token.morphs))
        ]
        # assumption 1: the sentence must include more than 1 EF's
        if not efs:
            raise EFNotIncludedError("|".join(["+".join(map(str, token.morphs)) for token in self.out]))
        # assumption 2: all EF's should be supported by KPS.
        for ef in efs:
            for pattern in self.HONORIFICS.keys():
                if self.matched(pattern, ef):
                    break
            else:
                raise EFNotSupportedError(ef)
        return self

    def conjugate(self, politeness: int):
        lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in self.out]
        out = list()
        for lex, morphs in lex2morphs:
            tuned = "+".join(morphs)
            for pattern in self.HONORIFICS.keys():
                if self.matched(pattern, tuned):
                    honorific = self.HONORIFICS[pattern][politeness]
                    tuned = tuned.replace(pattern, honorific)
                    self.logs.conjugations.add((pattern, honorific))
            # if something has changed, then go for it, but otherwise just use the lex.
            before = "".join([morph.split("/")[0] for morph in morphs])
            after = "".join([morph.split("/")[0] for morph in tuned.split("+")])
            if before != after:
                out.append(after)
            else:
                out.append(lex)
        self.out = " ".join(out)
        return self

    def abbreviate(self):
        for key, val in self.ABBREVIATIONS.items():
            if key in self.out:
                self.out = self.out.replace(key, val)
                self.logs.abbreviations.add((key, val))
        return self

    def irregulars(self):
        for key, val in self.IRREGULARS.items():
            if key in self.out:
                self.out = self.out.replace(key, val)
                self.logs.irregulars.add((key, val))
        return self

    # --- accessing options --- #
    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def environs(self):
        return pd.DataFrame(self.RULES).transpose().columns

    # --- supporting methods --- #
    @staticmethod
    def matched(pattern: str, string: str) -> bool:
        return True if re.match(f"(^|.*\\+){re.escape(pattern)}(\\+.*|$)", string) else False


class Translator:
    def __call__(self, sent: str) -> str:
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": os.environ['NAVER_CLIENT_ID'],
            "X-Naver-Client-Secret": os.environ['NAVER_CLIENT_SECRET']
        }
        data = {
            "source": "en",
            "target": "ko",
            "text": sent
        }
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        return r.json()['message']['result']['translatedText']


class Explainer:
    """
    This is here to explain each step in tuner. (mainly - apply_honorifics, apply_abbreviations, apply_irregulars).
    It is given a tuner as an input, attempts to explain the latest process.
    """

    def __init__(self, logs: Styler.Logs):
        self.logs = logs

    def __call__(self):
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    tbody th {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # --- step 1 ---
        msg_1 = "### 1️⃣ Politeness"
        politeness = self.logs.case['politeness']
        politeness = "casual style (-어)" if politeness == 1 \
            else "polite style (-어요)" if politeness == 2 \
            else "formal style (-습니다)"
        reason = self.logs.case['reason']
        msg_1 += f"\nYou should speak in a `{politeness}` to your `{self.logs.args['listener']}`" \
                 f" when you are in a `{self.logs.args['environ']}` environment."
        msg_1 += f"\n\n Why so? {reason}"
        st.markdown(msg_1)
        # --- step 2 ---
        msg_2 = f"### 2️⃣ Morphemes"
        before = self.logs.args['sent'].split(" ")
        after = ["".join(list(map(str, token.morphs))) for token in self.logs.steps[0]]
        df = pd.DataFrame(zip(before, after), columns=['before', 'after'])
        st.markdown(msg_2)
        st.markdown(df.to_markdown(index=False))
        # --- step 3 ---
        msg_3 = f"### 3️⃣ Honorifics"
        before = " ".join(["".join(list(map(str, token.morphs))) for token in self.logs.steps[0]])
        after = self.logs.steps[1]
        for key, val in self.logs.conjugations:
            before = before.replace(key, f"`{key}`")
            after = after.replace(val, f"`{val}`")
        df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
        st.markdown(msg_3)
        st.markdown(df.to_markdown(index=False))
        # # --- step 4 ---
        msg_4 = "### 4️⃣ Abbreviations"
        if len(self.logs.abbreviations) > 0:
            before = self.logs.steps[1]
            after = self.logs.steps[2]
            for key, val in self.styler.history_abbreviations:  # noqa
                before = before.replace(key, f"`{key}`")
                after = after.replace(val, f"`{val}`")
            st.markdown(msg_4)
            df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
            st.markdown(df.to_markdown(index=False))
        else:
            msg_4 += "\nNo abbreviation rules to be applied."
            st.markdown(msg_4)
        # # --- step 5 ---
        msg_5 = f"### 5️⃣ Conjugations"
        if len(self.logs.irregulars) > 0:
            before = self.logs.steps[2]
            after = self.logs.steps[3]
            for key, val in self.styler.history_irregulars:  # noqa
                before = before.replace(key, f"`{key}`")
                after = after.replace(val, f"`{val}`")
            st.markdown(msg_5)
            df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
            st.markdown(df.to_markdown(index=False))
        else:
            msg_5 += "\nNo conjugation rules to be applied."
            st.markdown(msg_5)
