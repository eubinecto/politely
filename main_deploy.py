"""
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
from politetune.processors import Tuner


# instantiate processors here
@st.cache(allow_output_mutation=True)
def cache_tuner() -> Tuner:
    return Tuner()


def main():
    # parsing the arguments
    tuner = cache_tuner()
    st.title("Politetune Demo")
    sent = st.text_input("Type a sentence here", value="나는 내 목표를 향해 달린다")
    listener = st.selectbox("Who is your listener?", tuner.listeners)
    visibility = st.selectbox("What is your visibility?", tuner.visibilities)

    if st.button(label="Tune"):
        with st.spinner("Please wait..."):
            tuned = tuner(sent, listener, visibility)
            st.write(tuned)


if __name__ == '__main__':
    main()
