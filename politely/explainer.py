from politely import Styler
import streamlit as st
import pandas as pd  # noqa


class Explainer:
    """
    This is here to explain each step in tuner. (mainly - apply_honorifics, apply_abbreviations, apply_irregulars).
    It is given a tuner as an input, attempts to explain the latest process.
    """

    def __init__(self, logs: Styler.Logs):
        self.logs = logs

    def __call__(self):
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
        politeness = self.logs.case['politeness']
        politeness = "casual style (-어)" if politeness == 1 \
            else "polite style (-어요)" if politeness == 2 \
            else "formal style (-습니다)"
        reason = self.logs.case['reason']
        msg_1 += f"\nYou should speak in a `{politeness}` to your `{self.logs.args['listener']}`" \
                 f" when you are in a `{self.logs.args['environ']}` environment."
        msg_1 += f"\n\n Why so? {reason}"
        st.markdown(msg_1)
        # --- step 2 ---
        msg_2 = f"### 2️⃣ Morphemes"
        before = self.logs.args['sent'].split(" ")
        after = ["".join(list(map(str, token.morphs))) for token in self.logs.steps[0]]
        df = pd.DataFrame(zip(before, after), columns=['before', 'after'])
        st.markdown(msg_2)
        st.markdown(df.to_markdown(index=False))
        # --- step 3 ---
        msg_3 = f"### 3️⃣ Honorifics"
        before = " ".join(["".join(list(map(str, token.morphs))) for token in self.logs.steps[0]])
        after = " ".join([
            "".join(elem) if isinstance(elem, list)
            else elem
            for elem in self.logs.steps[1]
        ])
        for key, val in self.logs.honorifics:
            before = before.replace(key, f"`{key}`")
            after = after.replace(val, f"`{val}`")
        df = pd.DataFrame(zip(before.split(" "), after.split(" ")), columns=['before', 'after'])
        st.markdown(msg_3)
        st.markdown(df.to_markdown(index=False))
        # # --- step 4 ---
        msg_4 = "### 4️⃣ Conjugations"
        st.markdown(msg_4)
        st.markdown("🚧 on development 🚧")
