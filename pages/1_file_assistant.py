import streamlit as st

from chat import asst_stream_response
from utils import check_password, get_client, get_assistants


def clear_thread():
    st.session_state["thread"] = st.session_state.client.beta.threads.create()
    st.session_state["messages"] = []
    if assistant_id := st.session_state.get("assistant_id"):
        st.session_state["instructions"] = ' '.join(
            ASSISTANTS[assistant_id].get('instructions', '').split())


if not check_password():
    st.stop()

st.session_state["client"] = get_client()
ASSISTANTS = get_assistants('assistants.yml')

st.header('Use an assistant with file search')

st.selectbox(
    label='Assistant',
    options=ASSISTANTS.keys(),
    format_func=lambda x: ASSISTANTS[x]['name'],
    index=None,
    key="assistant_id",
    placeholder="Select an assistant",
    label_visibility="collapsed",
    on_change=clear_thread,
)

if assistant_id := st.session_state.get("assistant_id"):
    st.html(ASSISTANTS[assistant_id]['description'])
    st.text_area(
        "System Prompt",
        key="instructions",
        help="Provide any specific instructions for the assistant that will apply to all queries.")

st.session_state["thread"] = st.session_state.get(
    "thread",
    st.session_state.client.beta.threads.create())

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    stream = asst_stream_response(
        client=st.session_state.client,
        thread=st.session_state.thread,
        assistant_id=assistant_id,
        prompt=prompt,
        instructions=st.session_state.instructions)

    stream_output = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": stream_output})
