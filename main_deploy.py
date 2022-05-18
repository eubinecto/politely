"""
It's okay to write dirty stuff, at least as of right now.
"""
from typing import Tuple
import streamlit as st
from politely import Styler, Explainer, Translator
from politely.errors import EFNotIncludedError, EFNotSupportedError


# instantiate processors here
@st.cache(allow_output_mutation=True)
def cache_resources() -> Tuple[Styler, Explainer, Translator]:
    styler = Styler()
    explainer = Explainer(styler.logs)
    translator = Translator()
    return styler, explainer, translator


def describe_case(styler: Styler, explainer: Explainer, sent: str, listener: str, environ: str):
    try:
        tuned = styler(sent, listener, environ)
    except EFNotIncludedError as e1:
        st.error("ERROR: " + str(e1))
    except EFNotSupportedError as e2:
        st.error("ERROR: " + str(e2))
    else:
        st.write(tuned)
        with st.expander("Need an explanation?"):
            explainer()


def main():
    # parsing the arguments
    styler, explainer, translator = cache_resources()
    st.title("Politely: an explainable Politeness Styler for the Korean language")
    desc = "- 💡: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) & [Eu-Bin KIM](https://github.com/eubinecto) @ the Univerity of Oxford\n" \
           "- ⚡️: [`khaiii`](https://github.com/kakao/khaiii) for analyzing Korean morphemes & [`papago`](https://papago.naver.com/?sk=auto&tk=ko&hn=1&st=hello%20world) for english-to-korean translations\n"\
           "- The code that runs this website is [publicly available on Github](https://github.com/eubinecto/kps). Please leave a ⭐ if you like what we are building!"
    st.markdown(desc)
    sent = st.text_input("Type an English sentence to translate", value="I run towards my goal")
    if st.button(label="Translate"):
        with st.spinner("Please wait..."):
            target = translator(sent)
            # 1
            listener = "friends and junior"
            st.header(f"`{listener}` 👥")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)
            # 2
            st.markdown("---")
            listener = "boss at work"
            st.header(f"`{listener}` 💼")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)
            # 3
            st.markdown("---")
            listener = "adult family"
            st.header(f"`{listener}` 👨‍👩‍👧‍👦")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, explainer, target, listener, environ)


if __name__ == '__main__':
    main()
