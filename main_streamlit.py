"""
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
from politetune.processors import Tuner, Highlighter


# instantiate processors here
tuner = Tuner()
highlighter = Highlighter()


def main():
    # parsing the arguments
    st.title("Politetune Demo")
    sent = st.text_input("Type a sentence here", value="나는 내 목표를 향해 달린다")
    listener = st.selectbox("Who is your listener?", highlighter.listeners)
    visibility = st.selectbox("What is your visibility?", highlighter.visibilities)

    if st.button(label="Tune"):
        with st.spinner("Please wait..."):
            tuned = tuner(sent, listener, visibility)
            st.markdown(tuned)
            # highlight the rule & honorifics that were applied
            left, center, right = st.columns(3)
            rule, honorifics, abbreviations = highlighter(tuner.rule, tuner.honorifics, tuner.abbreviations)
            left.table(rule)
            center.table(honorifics)
            right.table(abbreviations)


if __name__ == '__main__':
    main()
