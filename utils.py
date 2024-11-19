import hmac
import os

import yaml
from openai import OpenAI, OpenAIError
import streamlit as st


def get_client():
    if client := st.session_state.get("client"):
        return client
    else:
        try:
            return OpenAI(
                api_key=st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY"))
        except OpenAIError:
            st.error('Make sure environment variable OPENAI_API_KEY is set')
            st.stop()


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["PASSWORD"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def get_assistants(fname):
    """Read yaml file fname"""
    with open(fname, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        assistants = {}
        for key, d in data["ASSISTANTS"].items():
            if description := d.get("description"):
                d["description"] = description.format(**d.get('vars', {}))
            if d.get('active'):
                assistants[key] = d

        return assistants
