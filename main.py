"""
그냥 처음엔 막코딩하자. just put everything under here.
It's okay to write dirty stuff, at least as of right now.
"""
import streamlit as st
from politetune.honorifier import Honorifier


# instantiate a honorifier here
honorifier = Honorifier()


def main():
    # parsing the arguments
    st.title("Honorify Demo")
    sent = st.text_input("Type a sentence here", value="나는 공부해")
    listener = st.selectbox("Who is your listener?", honorifier.RULES.index)
    visibility = st.selectbox("What is your visibility?", honorifier.RULES.columns)

    if st.button(label="Honorify"):
        with st.spinner("Please wait..."):
            honorified, styler_rules, styler_honorifics = honorifier(sent, listener, visibility)
            st.markdown(honorified)
            left, right = st.columns(2)
            left.table(styler_rules)
            right.table(styler_honorifics)


if __name__ == '__main__':
    main()
