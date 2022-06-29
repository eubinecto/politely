"""
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
import pandas as pd
import os
import requests
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
    }
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return r.json()["message"]["result"]["translatedText"]


def explain(logs: dict):
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
    politeness = logs["__call__"]["in"]["politeness"]
    politeness = (
        "casual style (-어)"
        if politeness == 1
        else "polite style (-어요)"
        if politeness == 2
        else "formal style (-습니다)"
    )
    reason = logs["case"]["reason"]
    msg_1 += (
        f"\nYou should speak in a `{politeness}` to your `{logs['listener']}`"
        f" when you are in a `{logs['environ']}` environment."
    )
    msg_1 += f"\n\n Why so? {reason}"
    st.markdown(msg_1)
    # --- step 2 ---
    msg_2 = f"### 2️⃣ Morphemes"
    before = logs["__call__"]["in"]["sent"].split(" ")
    after = ["".join(list(map(str, token.morphs))) for token in logs["analyze"]["out"]]
    df = pd.DataFrame(zip(before, after), columns=["before", "after"])
    st.markdown(msg_2)
    st.markdown(df.to_markdown(index=False))
    # --- step 3 ---
    msg_3 = f"### 3️⃣ Honorifics"
    before = " ".join(["".join(list(map(str, token.morphs))) for token in logs["analyze"]["out"]])
    after = " ".join(["".join(elem) if isinstance(elem, list) else elem for elem in logs["honorify"]["out"]])
    for key, val in logs["honorifics"]:
        before = before.replace(key, f"`{key}`")
        after = after.replace(val, f"`{val}`")
    df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=["before", "after"])
    st.markdown(msg_3)
    st.markdown(df.to_markdown(index=False))
    # # --- step 4 ---
    msg_4 = "### 4️⃣ Conjugations"
    st.markdown(msg_4)
    st.markdown("🚧 on development 🚧")


def describe_case(styler: Styler, sent: str, listener: str, environ: str):
    try:
        case = RULES[listener][environ]
        tuned = styler(sent, case["politeness"])
    except EFNotIncludedError as e1:
        st.error("ERROR: " + str(e1))
    except EFNotSupportedError as e2:
        st.error("ERROR: " + str(e2))
    else:
        st.write(tuned)
        with st.expander("Need an explanation?"):
            styler.logs.update({"listener": listener, "environ": environ, "case": case})
            explain(styler.logs)


def main():
    # parsing the arguments
    st.title("Politely: an explainable Politeness Styler for the Korean language")
    desc = (
        "- 💡: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) & [Eu-Bin"
        " KIM](https://github.com/eubinecto) @ the Univerity of Oxford\n- ⚡️:"
        " [`khaiii`](https://github.com/kakao/khaiii) for analyzing Korean morphemes &"
        " [`papago`](https://papago.naver.com/?sk=auto&tk=ko&hn=1&st=hello%20world) for"
        " english-to-korean translations\n- The code that runs this website is"
        " [publicly available on Github](https://github.com/eubinecto/kps). Please"
        " leave a ⭐ if you like what we are building!"
    )
    st.markdown(desc)
    sent = st.text_input("Type an English sentence to translate", value="I run towards my goal")
    styler = Styler()
    if st.button(label="Translate"):
        with st.spinner("Please wait..."):
            target = translate(sent)
            # 1
            listener = "friends and junior"
            st.header(f"`{listener}` 👥")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)
            # 2
            st.markdown("---")
            listener = "boss at work"
            st.header(f"`{listener}` 💼")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)
            # 3
            st.markdown("---")
            listener = "adult family"
            st.header(f"`{listener}` 👨‍👩‍👧‍👦")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, target, listener, environ)


if __name__ == "__main__":
    main()
