import streamlit as st

st.set_page_config(
    page_title="API Assistants",
)

with open('Home.md', encoding='utf-8') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
