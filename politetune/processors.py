import itertools
import pandas as pd
from khaiii.khaiii import KhaiiiApi
from typing import Optional, Any, Callable, List
from politetune.fetchers import fetch_abbreviations, fetch_honorifics, fetch_rules, fetch_irregulars
import streamlit as st


class Tuner:
    """
    a politeness tuner.
    """
    ABBREVIATIONS: dict = fetch_abbreviations()
    HONORIFICS: dict = fetch_honorifics()
    RULES: dict = fetch_rules()
    IRREGULARS: dict = fetch_irregulars()

    def __init__(self):
        self.khaiii = KhaiiiApi()
        # inputs
        self.sent: Optional[str] = None
        self.listener: Optional[str] = None
        self.environ: Optional[str] = None
        # the output can be anything
        self.out: Any = None
        self.logs: list = list()
        self.history_honorifics: set = set()
        self.history_abbreviations: set = set()
        self.history_irregulars: set = set()

    def __call__(self, sent: str, listener: str, environ: str) -> str:
        # register inputs
        self.sent = sent
        self.listener = listener
        self.environ = environ
        # process each step
        for step in self.steps():
            step()
        # return the final output
        return self.out

    def steps(self) -> List[Callable]:
        return [
            self.clear,
            self.preprocess,
            self.analyze_morphemes,
            self.log,
            self.apply_honorifics,
            self.log,
            self.apply_abbreviations,
            self.log,
            self.apply_irregulars,
            self.log,
            self.postprocess
        ]

    def clear(self):
        self.logs.clear()
        self.history_honorifics.clear()
        self.history_abbreviations.clear()
        self.history_irregulars.clear()

    def log(self):
        self.logs.append(self.out)

    def preprocess(self):
        self.out = self.sent + "." if not self.sent.endswith(".") else self.sent  # for accurate pos-tagging

    def analyze_morphemes(self):
        tokens = self.khaiii.analyze(self.out)
        self.out = tokens

    def apply_honorifics(self):
        politeness = self.RULES[self.listener][self.environ]['politeness']
        lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in self.out]
        out = list()
        for lex, morphs in lex2morphs:
            # this is to be used just for matching
            substrings = ["+".join(morphs[i:j]) for i, j in itertools.combinations(range(len(morphs) + 1), 2)]
            if set(substrings) & set(self.HONORIFICS.keys()):  # need to make sure any patterns match any substring.
                tuned = "+".join(morphs)
                for pattern in self.HONORIFICS.keys():
                    honorific = self.HONORIFICS[pattern][politeness]
                    if pattern in tuned:
                        tuned = tuned.replace(pattern, honorific)
                        self.history_honorifics.add((pattern, honorific))  # to be used in the explainer
                tuned = "".join([token.split("/")[0] for token in tuned.split("+")])
                out.append(tuned)
            else:
                out.append(lex)
        self.out = " ".join(out)

    def apply_abbreviations(self):
        for key, val in self.ABBREVIATIONS.items():
            if key in self.out:
                self.out = self.out.replace(key, val)
                self.history_abbreviations.add((key, val))

    def apply_irregulars(self):
        for key, val in self.IRREGULARS.items():
            if key in self.out:
                self.out = self.out.replace(key, val)
                self.history_irregulars.add((key, val))

    def postprocess(self):
        self.out = self.out if self.sent.endswith(".") else self.out[:-1]

    @property
    def listeners(self):
        return pd.DataFrame(self.RULES).transpose().index

    @property
    def environs(self):
        return pd.DataFrame(self.RULES).transpose().columns


class Explainer:
    """
    This is here to explain each step in tuner. (mainly - apply_honorifics, apply_abbreviations, apply_irregulars).
    It is given a tuner as an input, attempts to explain the latest process.
    """
    def __init__(self, tuner: Tuner):
        self.tuner = tuner

    def __call__(self, *args, **kwargs):
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
        msg_1 = "### 1️⃣ Determine the level of politeness"
        politeness = self.tuner.RULES[self.tuner.listener][self.tuner.environ]['politeness']
        politeness = "no honorifics (-어)" if politeness == 1\
            else "polite honorifics (-어요)" if politeness == 2\
            else "formal honorifics (-습니다)"
        reason = self.tuner.RULES[self.tuner.listener][self.tuner.environ]['reason']
        msg_1 += f"\nYou should speak with `{politeness}` to your `{self.tuner.listener}`" \
                 f" when you are in a `{self.tuner.environ}` environment."
        msg_1 += f"\n\n Why so? {reason}"
        st.markdown(msg_1)
        # --- step 2 ---
        msg_2 = f"### 2️⃣ Analyze morphemes"
        before = self.tuner.sent.split(" ")
        after = ["".join(list(map(str, token.morphs))) for token in self.tuner.logs[0]]
        df = pd.DataFrame(zip(before, after), columns=['before', 'after'])
        st.markdown(msg_2)
        st.markdown(df.to_markdown(index=False))
        # --- step 3 ---
        msg_3 = f"### 3️⃣ Apply honorifics"
        before = " ".join(["".join(list(map(str, token.morphs))) for token in self.tuner.logs[0]])
        after = self.tuner.logs[1]
        for key, val in self.tuner.history_honorifics:
            before = before.replace(key, f"`{key}`")
            after = after.replace(val, f"`{val}`")
        df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
        st.markdown(msg_3)
        st.markdown(df.to_markdown(index=False))
        # # --- step 4 ---
        msg_4 = "### 4️⃣ Apply abbreviations"
        if len(self.tuner.history_abbreviations) > 0:
            before = self.tuner.logs[1]
            after = self.tuner.logs[2]
            for key, val in self.tuner.history_abbreviations:  # noqa
                before = before.replace(key, f"`{key}`")
                after = after.replace(val, f"`{val}`")
            st.markdown(msg_4)
            df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
            st.markdown(df.to_markdown(index=False))
        else:
            msg_4 += "\nNo abbreviation rules to be applied."
            st.markdown(msg_4)
        # # --- step 5 ---
        msg_5 = f"### 5️⃣ Apply irregular conjugations"
        if len(self.tuner.history_irregulars) > 0:
            before = self.tuner.logs[2]
            after = self.tuner.logs[3]
            for key, val in self.tuner.history_irregulars:  # noqa
                before = before.replace(key, f"`{key}`")
                after = after.replace(val, f"`{val}`")
            st.markdown(msg_5)
            df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
            st.markdown(df.to_markdown(index=False))
        else:
            msg_5 += "\nNo conjugation rules to be applied."
            st.markdown(msg_5)
