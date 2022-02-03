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
    listener = st.selectbox("Who is your listener?", honorifier.rules.keys())
    visibility = st.selectbox("What is your visibility?", honorifier.visibilities)

    if st.button(label="Honorify"):
        honorified = honorifier(sent, listener, visibility)
        msg = "yes" if honorifier.honored else "no"
        st.markdown(f"Should you use honorifics?: `{msg}`")
        st.markdown(honorified)


if __name__ == '__main__':
    main()
