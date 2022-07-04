"""
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
import pandas as pd  # noqa
import os
import requests  # noqa
from politely import Styler, RULES
from politely.errors import EFNotIncludedError, EFNotSupportedError


def translate(sent: str) -> str:
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": os.environ["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": os.environ["NAVER_CLIENT_SECRET"],
    }
    data = {
        "source": "en",
        "target": "ko",
        "text": sent,
        "honorific": False
    }
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
    msg = "### 1️⃣ Translate the sentence"
    before = eng
    after = logs["__call__"]["in"]['sent']
    df = pd.DataFrame([(before, after)], columns=["before",  "after"])
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
    before = logs["__call__"]["in"]['sent']
    after = logs["analyze"]["out"].replace("+", " ")
    df = pd.DataFrame([(before, after)], columns=["before",  "after"])
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))
    # --- step 4 ---
    msg = f"### 4️⃣ Apply honorifics"
    before = logs["analyze"]["out"]
    after = logs["honorify"]["out"]
    for key, val in logs["honorifics"]:
        before = before.replace(key, f"`{key.replace('+', '')}`")
        after = after.replace(val, f"`{val.replace('+', '')}`")
    df = pd.DataFrame(zip(before.split("+"), after.split("+")), columns=["before", "after"])
    st.markdown(msg)
    st.markdown(df.to_markdown(index=False))
    # # --- step 5 ---
    msg = "### 5️⃣ Conjugate morphemes"
    before = logs["analyze"]["out"].replace("+", " ")
    after = logs["conjugate"]["out"]
    df = pd.DataFrame([(before, after)], columns=["before",  "after"])
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
    eng = st.text_input("Type an English sentence to translate with honorifics", value="I run towards my goal")
    styler = Styler()
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
