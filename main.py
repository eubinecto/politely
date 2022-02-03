"""
그냥 처음엔 막코딩하자. just put everything under here.
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
import platform
from typing import Dict, Tuple, List
from konlpy.tag import Okt


# verb -> visibility -> unhonored form / honored form
# TODO: The keys should be changed to regular expressions
VERB_HONORIFICS: Dict[str, Tuple[str, str]] = {
    # just do one thing and one thing right.
    "하다": ("해", "해요"),  # should be at the end.
    "마시다": ("마셔", "마셔요"),
    "알다": ("알아", "알아요"),
    "있다": ("있어", "있어요"),
    "모르다": ("몰라", "몰라요"),
    "들다": ("들어", "들어요"),
    "사다": ("사", "사요"),
    "보다": ("봐", "봐요"),
    "가다": ("가", "가요"),
    "오다": ("와", "와요"),
    "아프다": ("아파", "아파요"),
    "목마르다": ("목말라", "목말라요"),
    "배고프다": ("배고파", "배고파요"),
    "고맙다": ("고마워", "고마워요"),
}

NOUN_HONORIFICS: Dict[str, Tuple[str, str]] = {
    "나": ("나", "저"),
    "저": ("나", "저"),
}


VISIBILITIES = [
    "private",
    "public"
]

# listener -> visibility -> not honored / honored
# you choose a listener
RULES: Dict[str, Tuple[int, int]] = {
    "teacher": (1, 1),
    "boss at work": (1, 1),
    "older sister": (0, 0),
    "older brother": (0, 0),
    "older cousin": (0, 0),
    "younger sister": (0, 0),
    "younger brother": (0, 0),
    "younger cousin": (0, 0),
    "uncle": (1, 1),
    "friend": (0, 1),
    "grandpa": (1, 1),
    "grandma": (1, 1),
    "mum": (0, 1),
    "dad": (1, 1),
    "shop clerk": (1, 1)
}


class Honorifier:

    def __init__(self, okt: Okt):
        self.okt = okt

    def __call__(self, sent: str, honored: bool) -> str:
        # wait, this way, I cannot deal with the white spaces
        lemmas: List[str] = self.okt.morphs(sent, stem=True)
        tok2pos: List[Tuple[str, str]] = self.okt.pos(sent)
        for lemma, (token, pos) in zip(lemmas, tok2pos):
            if pos == "Verb" and lemma in VERB_HONORIFICS:
                sent = sent.replace(token, f"`{VERB_HONORIFICS[lemma][honored]}({pos})`")
            elif pos == "Noun" and lemma in NOUN_HONORIFICS:
                sent = sent.replace(token, f"`{NOUN_HONORIFICS[lemma][honored]}({pos})`")
        return sent


def load_okt() -> Okt:
    if platform.processor() == "arm":
        okt = Okt(jvmpath='/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java')  # m1-compatible jvm
    else:
        okt = Okt()
    return okt


honorifier = Honorifier(load_okt())


def main():
    # parsing the arguments
    st.title("Honorify Demo")
    sent = st.text_input("Type a sentence here", value="나는 공부해")
    listener = st.selectbox("Who is your listener?", RULES.keys())
    visibility = st.selectbox("What is your visibility?", VISIBILITIES)

    if st.button(label="Honorify"):
        honored = RULES[listener][VISIBILITIES.index(visibility)]
        msg = "yes" if honored else "no"
        st.markdown(f"Should you use honorifics?: `{msg}`")
        honorified = honorifier(sent, honored)
        st.markdown(honorified)


if __name__ == '__main__':
    main()
