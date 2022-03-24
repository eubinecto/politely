"""
It's okay to write dirty stuff, at least as of right now.
"""
from typing import Tuple
import streamlit as st
from politetune.processors import Tuner, Explainer


# instantiate processors here
@st.cache(allow_output_mutation=True)
def cache_resources() -> Tuple[Tuner, Explainer]:
    tuner = Tuner()
    explainer = Explainer(tuner)
    return tuner, explainer


def main():
    # parsing the arguments
    tuner, explainer = cache_resources()
    st.title("Politetune")
    sent = st.text_input("Type a sentence here", value="나는 내 목표를 향해 달린다")
    listener = st.selectbox("Who is your listener?", tuner.listeners)
    environ = st.selectbox("How do you find the environment you are speaking in?", tuner.environs)

    if st.button(label="Tune"):
        with st.spinner("Please wait..."):
            tuned = tuner(sent, listener, environ)
            st.write(tuned)
            with st.expander("Need an explanation?"):
                for msg in explainer():
                    st.markdown(msg)


if __name__ == '__main__':
    main()
