import inspect
import os
import re
import requests  # noqa
import pandas as pd  # noqa
import streamlit as st
from khaiii.khaiii import KhaiiiApi
from typing import Any, Tuple, Set
from soynlp.hangle import compose, decompose
from politely.fetchers import fetch_honorifics, fetch_rules
from politely.errors import EFNotIncludedError, EFNotSupportedError
from multipledispatch import dispatch
from dataclasses import dataclass, field
from soynlp.lemmatizer import conjugate as soynlp_conjugate


class Styler:
    """
    A rule-based Korean Politeness Styler
    """
    @dataclass
    class Logs:
        args: dict = field(default_factory=dict)
        case: dict = field(default_factory=dict)
        steps: list = field(default_factory=list)
        honorifics: Set[Tuple[str, str]] = field(default_factory=set)
        conjugations: Set[Tuple[str, str, str, str]] = field(default_factory=set)
    # class-owned attributes
    RULES: dict = fetch_rules()
    HONORIFICS: dict = fetch_honorifics()

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
            .honorify(politeness) \
            .log() \
            .conjugate() \
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
        self.logs.honorifics.clear()
        self.logs.conjugations.clear()
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

    def honorify(self, politeness: int):
        lex2morphs = [(token.lex, list(map(str, token.morphs))) for token in self.out]
        self.out = list()
        for lex, morphs in lex2morphs:
            tuned = "+".join(morphs)
            for pattern in self.HONORIFICS.keys():
                if self.matched(pattern, tuned):
                    honorific = self.HONORIFICS[pattern][politeness]
                    tuned = tuned.replace(pattern, honorific)
                    self.logs.honorifics.add((pattern, honorific))
            # if something has changed, then go for it, but otherwise just use the lex.
            before = [morph.split("/")[0] for morph in morphs]
            after = [morph.split("/")[0] for morph in tuned.split("+")]
            if "".join(before) != "".join(after):
                self.out.append(after)
            else:
                self.out.append(lex)
        return self

    def conjugate(self):
        """
        conjugate L -> R.
        Custom rules are followed by soynlp's rules.
        """
        out = list()
        for chunk in self.out:
            if isinstance(chunk, list):
                # you should conjugate these
                left = chunk[0]
                for i in range(len(chunk) - 1):
                    right = chunk[i + 1]
                    r_first = right[0]
                    l_last = left[-1]
                    l_cho, l_jung, l_jong = decompose(l_last)  # decompose the last element
                    r_cho, r_jung, r_jong = decompose(r_first)  # decompose the first element
                    if l_jong == " " and right.startswith("ㅂ니"):
                        # e.g. 전 이제 떠나ㅂ니다 -> 전 이제 떠납니다
                        left = left[:-1] + compose(l_cho, l_jung, "ㅂ")
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"어간에 받침이 없고 어미가 읍인 경우, ㅂ은 어간의 받침으로 쓰임"))
                    elif l_jong != " " and right.startswith("ㅂ니"):
                        # e.g. 갔ㅂ니다 -> 갔습니다
                        left += f"습{right[1:]}"
                        self.logs.conjugations.add((l_last, r_first, left, f"종성있음 + `ㅂ니` -> 습니"))
                    elif l_jong != " " and right.startswith("ㅂ시"):
                        # 줍은 예외
                        if left == "줍":
                            left = left[:-1] + "주웁"
                            left += right[1:]
                            self.logs.conjugations.add((l_last, r_first, left, f"줍 예외"))
                        else:
                            # e.g. 먹ㅂ시다
                            left += f"읍{right[1:]}"
                            self.logs.conjugations.add((l_last, r_first, left, f"종성있음 + `ㅂ시` -> 읍니"))
                    elif l_jong == "ㅎ" and r_first == "어":
                        # e.g. 어떻 + 어요 -> 어때요, 좋어요 -> 좋아요
                        left = left[:-1] + compose(l_cho, "ㅐ",  " ")
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㅎ` + `어` -> `ㅐ`"))
                    elif l_jung == "ㅣ" and l_jong == " " and r_first == "어":
                        # e.g. 시어 -> 셔
                        # 하지만 e.g. 있어 -> 있어
                        left = left[:-1] + compose(l_cho, "ㅕ",  " ")
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㅣ`+ `ㅓ` -> `ㅕ`"))
                    elif l_jung == "ㅏ" and l_jong in ("ㄷ", "ㅌ") and r_first == "어":
                        # e.g. 같어요 -> 같아요
                        # e.g  닫어요 -> 닫아요
                        left += f"아{right[1:]}"
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㅏ (종성o)`+ `ㅓ` -> `ㅕ`"))
                    elif l_last == "하" and r_jung in ("ㅓ", "ㅕ"):
                        # e.g. 하어요 -> 해요, 하여요 -> 해요, 하었어요 -> 했어요  -> 하였어요 -> 했어요
                        left = left[:-1] + compose(l_cho, "ㅐ",  r_jong)
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"`하`+ (`ㅓ` 또는 `ㅕ`) -> `해`"))
                    elif l_jung == "ㅏ" and r_first == "의":
                        # e.g. 나의 -> 내 ("내"가 더 많이 쓰이므로)
                        left = left[:-1] + compose(l_cho, "ㅐ",  " ")
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㅏ`+ `의` -> `ㅐ`"))
                    elif l_jung == "ㅓ" and r_first == "의":
                        # e.g. 저의 -> 제 ("제"가 더 많이 쓰이므로)
                        left = left[:-1] + compose(l_cho, "ㅔ",  " ")
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㅓ`+ `의` -> `ㅔ`"))
                    elif l_jung == "ㅓ" and l_jong == " " and r_first == "이":
                        # e.g. 거이죠 -> 거죠?
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"ㅓ+ 이 -> ㅓ (이 탈락)"))
                    elif l_jong == 'ㄷ' and r_cho == "ㅇ":
                        # e.g. 깨닫아 -> 깨달아
                        left = left[:-1] + compose(l_cho, l_jung,  "ㄹ")
                        left += right
                        self.logs.conjugations.add((l_last, r_first, left, f"`ㄷ` 종성 + `ㅇ` 초성 -> `ㄹ` 종성"))
                    elif l_jung == "ㅏ" and l_jong == " " and r_first == "어":
                        left += right[1:]
                        self.logs.conjugations.add((l_last, r_first, left, f"동모음 탈락"))
                    else:
                        # rely on soynlp for the remaining cases
                        # always pop the shortest one (e.g. 마시어, 마셔, 둘 중 하나일 경우 마셔를 선택)
                        # warning - popping an element from the set maybe non-deterministic
                        left = min(soynlp_conjugate(left, right), key=lambda x: len(x))
                        self.logs.conjugations.add((l_last, r_first, left, f"conjugations done by soynlp"))
                # after the for loop ends
                out.append(left)
            else:
                out.append(chunk)
        self.out = " ".join(out)
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
            "text": sent,
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
        after = " ".join([
            "".join(elem) if isinstance(elem, list)
            else elem
            for elem in self.logs.steps[1]
        ])
        for key, val in self.logs.honorifics:
            before = before.replace(key, f"`{key}`")
            after = after.replace(val, f"`{val}`")
        df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
        st.markdown(msg_3)
        st.markdown(df.to_markdown(index=False))
        # # --- step 4 ---
        msg_4 = "### 4️⃣ Conjugations"
        st.markdown(msg_4)
        st.markdown("🚧 on development 🚧")
