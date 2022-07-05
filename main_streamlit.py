"""
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
import pandas as pd  # noqa
import os
import requests  # noqa
import yaml  # noqa
from politely import Styler, DEL
from politely.errors import EFNotIncludedError, EFNotSupportedError


# --- constants --- #

RULES_YAML_STR = """friends and junior:
  comfortable & informal:
    politeness: 1
    reason: A comfortable and informal situation is a very relaxed situation for all, so you may speak to your friends and juniors in a casual style (`-어`).
  formal:
    politeness: 2
    reason: If there are observers around or the situation is rather formal, then you and your listener may not find it completely relaxing. If so, you should speak in a polite style (`-어요`) even when you are speaking to your friends and juniors.
boss at work:
  comfortable & informal:
    politeness: 2
    reason: If you are in an informal situation with your boss, e.g. a company dinner, then you and your boss may find it a little more relaxing than at the work place. Therefore, it is not necessary to speak in a formal style, and you may speak to your boss in a polite style (`-어요`).
  formal:
    politeness: 3
    reason: If you are in a highly formal environment, e.g. an important meeting, you should always speak in a formal style (`-읍니다`). This shows the appropriate respect to your listeners in a high-profile context.
adult family:
  comfortable & informal:
    politeness: 1
    reason: If you are in a relaxed setting, it is customary and allowed to speak to your family members in a casual style (`-어`) even when they are older than you.
  formal:
    politeness: 2
    reason: If someone outside of your family, e.g. a neighbour, is partaking the conversation too, then it is customary to speak to your family in a polite style (`-어요`) so that you and your family come acorss polite to the outsiders."""
RULES = yaml.safe_load(RULES_YAML_STR)
LISTENERS = pd.DataFrame(RULES).transpose().index.tolist()
ENVIRONS = pd.DataFrame(RULES).transpose().columns.tolist()


def translate(text: str) -> str:
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": os.environ["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": os.environ["NAVER_CLIENT_SECRET"],
    }
    data = {"source": "en", "target": "ko", "text": text, "honorific": False}
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return r.json()["message"]["result"]["translatedText"]


def explain(logs: dict, eng: str):
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
    msg = "### 1️⃣ Translate the textence"
    before = eng
    after = logs["__call__"]["in"]["text"]
    df = pd.DataFrame([(before, after)], columns=["before", "after"])
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))
    # --- step 2 ---
    msg = "### 2️⃣ Determine politeness"
    politeness = logs["__call__"]["in"]["politeness"]
    politeness = (
        "casual style (-어)"
        if politeness == 1
        else "polite style (-어요)"
        if politeness == 2
        else "formal style (-습니다)"
    )
    reason = logs["case"]["reason"]
    msg += (
        f"\nYou should speak in a `{politeness}` to your `{logs['listener']}`"
        f" when you are in a `{logs['environ']}` environment."
    )
    msg += f"\n\n Why so? {reason}"
    st.markdown(msg)
    # --- step 3 ---
    msg = f"### 3️⃣ Analyze morphemes"
    before = logs["__call__"]["in"]["text"]
    after = logs["analyze"]["out"].replace(DEL, " ")
    df = pd.DataFrame([(before, after)], columns=["before", "after"])
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))
    # --- step 4 ---
    msg = f"### 4️⃣ Apply honorifics"
    before = logs["analyze"]["out"]
    after = logs["honorify"]["out"]
    df = pd.DataFrame(
        zip(before.split(DEL), after.split(DEL)), columns=["before", "after"]
    )
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))
    # # --- step 5 ---
    msg = "### 5️⃣ Conjugate morphemes"
    before = logs["analyze"]["out"].replace(DEL, " ")
    after = logs["conjugate"]["out"]
    df = pd.DataFrame([(before, after)], columns=["before", "after"])
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))


def describe_case(styler: Styler, eng: str, kor: str, listener: str, environ: str):
    try:
        case = RULES[listener][environ]
        tuned = styler(kor, case["politeness"])
    except EFNotIncludedError as e1:
        st.error("ERROR: " + str(e1))
    except EFNotSupportedError as e2:
        st.error("ERROR: " + str(e2))
    else:
        st.write(tuned)
        with st.expander("Need an explanation?"):
            styler.logs.update({"listener": listener, "environ": environ, "case": case})
            explain(styler.logs, eng)


def main():
    # parsing the arguments
    st.title("Politely: an explainable Politeness Styler for the Korean language")
    desc = (
        "- 💡: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) & [Eu-Bin"
        " KIM](https://github.com/eubinecto) @ the Univerity of Oxford\n- ⚡️:"
        " [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) for analyzing Korean morphemes &"
        " [`papago`](https://papago.naver.com/?sk=auto&tk=ko&hn=1&st=hello%20world) for"
        " english-to-korean translations\n- The code that runs this website is"
        " [publicly available on Github](https://github.com/eubinecto/kps). Please"
        " leave a ⭐ if you like what we are building!"
    )
    st.markdown(desc)
    eng = st.text_input(
        "Type an English textence to translate with honorifics",
        value="I run towards my goal",
    )
    styler = Styler(debug=True)
    if st.button(label="Translate"):
        with st.spinner("Please wait..."):
            kor = translate(eng)
            # 1
            listener = "friends and junior"
            st.header(f"`{listener}` 👥")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            # 2
            st.markdown("---")
            listener = "boss at work"
            st.header(f"`{listener}` 💼")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            # 3
            st.markdown("---")
            listener = "adult family"
            st.header(f"`{listener}` 👨‍👩‍👧‍👦")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)


if __name__ == "__main__":
    main()
