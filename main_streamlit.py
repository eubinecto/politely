"""
그냥 처음엔 막코딩하자. just put everything under here.
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
import pandas as pd
from politetune.tuner import Tuner


# instantiate a honorifier here
tuner = Tuner()


def main():
    # parsing the arguments
    rules = pd.DataFrame(tuner.RULES).transpose()
    st.title("Politetune Demo")
    sent = st.text_input("Type a sentence here", value="나는 내 목표를 향해 달린다")
    listener = st.selectbox("Who is your listener?", rules.index)
    visibility = st.selectbox("What is your visibility?", rules.columns)

    if st.button(label="Tune"):
        with st.spinner("Please wait..."):
            res = tuner(sent, listener, visibility)
            st.markdown(res['tuned'])
            left, right = st.columns(2)
            left.table(res['rules'])
            right.table(res['honorifics'])
            # can you highlight abbreviations as well?


if __name__ == '__main__':
    main()
