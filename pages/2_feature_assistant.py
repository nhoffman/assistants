from enum import Enum
import json

import streamlit as st

import chat
from utils import check_password, get_client

st.set_page_config(layout="wide")


class ParameterType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    # OBJECT = "object"


def getval(key, default=None):
    return st.session_state.get(key, default)


def unwrap(text):
    return ' '.join(text.split())


def submit_query():
    if getval("context"):
        try:
            response = chat.get_features(
                getval("client"),
                getval('context'),
                getval('prompt'),
                tools=[getval('tool_spec')],
                model='gpt-4o')
            st.session_state['response'] = response
        except Exception as e:
            st.error(e)


if not check_password():
    st.stop()

st.session_state["client"] = get_client()

st.header('Feature extraction using OpenAI function calling')

with st.form("content_form"):
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        context = st.text_area(
            "Document Content", key="context",
            # value=test_chat.context,
            placeholder="Enter the document content here"
        )
    with form_col2:
        prompt = st.text_area(
            "Prompt", key="prompt",
            # value=test_chat.prompt,
            placeholder=unwrap(
                """Optional. Use this area to provide additional
                instructions or examples for representing the output.
                """))

        submitted = st.form_submit_button("Submit", on_click=submit_query)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Function Definition", divider=True)
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        func_name = st.text_input(
            "Function name", key="func_name",
            placeholder="lowercase_with_underscores")
    with subcol2:
        number_of_features = st.number_input(
            "Number of features", value=1, min_value=1, max_value=10,
        )

    func_desc = st.text_area(
        "Function description", key="func_desc", height=68,
        placeholder=unwrap("""
        Describe the purpose of this function. This description will
        be used to determine the context in which the function is
        called.
        """))

    for i in range(1, number_of_features + 1):
        if feat_name := getval(f"feat_name_{i}"):
            st.subheader(f"Feature {i}: {feat_name}", divider=True)
        else:
            st.subheader(f"Feature {i}", divider=True)

        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            st.text_input(
                "Feature name", key=f"feat_name_{i}",
                placeholder="lowercase_with_underscores")
        with subcol2:
            st.selectbox(
                "Feature type", key=f"feat_type_{i}",
                options=[t.value for t in ParameterType])
        with subcol3:
            st.toggle("Required", key=f"feat_required_{i}")

        if getval(f"feat_type_{i}") == ParameterType.STRING.value:
            st.text_input(
                "Enum values", key=f"feat_enum_vals_{i}",
                placeholder="Comma-separated list of values")

        st.text_area(
            "Feature description", key=f"feat_description_{i}", height=68,
            placeholder=unwrap(
                """Describe the feature to be extracted into this field.
                """))

with col2:
    # assemble the tool specification
    properties = {}
    required = []
    for i in range(1, number_of_features + 1):
        property = {
            "type": getval(f"feat_type_{i}"),
            "description": getval(f"feat_description_{i}")
        }
        if enum_vals := getval(f"feat_enum_vals_{i}"):
            property["enum"] = [s.strip() for s in enum_vals.split(",")]

        feat_name = getval(f"feat_name_{i}") or f"feat_name_{i}"
        properties[feat_name] = property
        if getval(f"feat_required_{i}", False):
            required.append(feat_name)

    st.session_state['tool_spec'] = {
        "type": "function",
        "function": {
            "name": func_name or "function_name",
            "description": func_desc,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

    # display the pretty-printed value of tool_spec
    if submitted:
        st.dataframe(getval('response'))

    spec_json = json.dumps(st.session_state['tool_spec'], indent=2)
    st.markdown(f"```json\n{spec_json}\n```")
