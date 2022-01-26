"""
그냥 처음엔 막코딩하자. just put everything under here.
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
from typing import Dict, Tuple
from konlpy.tag import Okt
import copy


RULES: Dict[str, Tuple[int, int]] = {
    "teacher": (1, 1),  # teacher
    "boss at work": (1, 1),  # boss at work
    "older sister": (0, 0),  # older sister
    "older brother": (0, 0),  # older brother
    "older cousin": (0, 0),  # older cousin
    "younger sister": (0, 0),  # younger sister
    "younger brother": (0, 0),  # younger brother
    "younger cousin": (0, 0),  # younger cousin
    "uncle": (1, 1),  # uncle
    "friend": (0, 1),  # friend
    "grandpa": (1, 1),  # grandpa
    "grandma": (1, 1),  # grandma
    "mum": (0, 1),  # mum
    "dad": (1, 1),  # dad
    "shop clerk": (1, 1)  # shop clerk
}


HONORIFICS: Dict[str, Tuple[str, str]] = {
    "하다": ("해", "해요"),  # this covers pretty much all the -하다 verbs.
    "마시다": ("마셔", "마셔요"),
    "알다": ("알아", "알아요"),
    "모르다": ("몰라", "몰라요"),
    "듣다": ("들어", "들어요"),
    "사다": ("사", "사요"),
    "보다": ("봐", "봐요"),
    "가다": ("가", "가요"),
    "오다": ("와", "와요"),
    "아프다": ("아파", "아파요"),
    "목마르다": ("목말라", "목말라요"),
    "배고프다": ("배고파", "배고파요"),
    "고맙다": ("고마워", "고마워요")
}

VISIBILITIES = [
    "private",
    "public"
]


def main():
    # parsing the arguments
    st.title("Politetune Demo")
    sent = st.text_input("Type a sentence you want to politetune", "나는 공부한다")
    listener = st.sidebar.selectbox("Who is your listener?", RULES.keys())
    visibility = st.sidebar.selectbox("How visible are you?", VISIBILITIES)
    visibility = VISIBILITIES.index(visibility)
    # decide if you should be polite or not
    polite = RULES[listener][visibility]
    # first, tokenize & lemmatize words
    okt = Okt()
    # then, polite-tune the tokens.
    tuned = copy.copy(sent)
    for token, lemma in zip(okt.morphs(sent, stem=False), okt.morphs(sent, stem=True)):
        if lemma in HONORIFICS.keys() and token != HONORIFICS[lemma][polite]:
            tuned = tuned.replace(token, HONORIFICS[lemma][polite])
    # print out the results
    st.write(f"tuned: {tuned}")
    st.write(f"politeness: {polite}")


if __name__ == '__main__':
    main()
