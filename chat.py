import logging
import json

from openai import OpenAI, AssistantEventHandler
from openai.types.beta.assistant_stream_event import ThreadMessageDelta

log = logging.getLogger(__name__)

ldt_rule = 'https://www.federalregister.gov/documents/2024/05/06/2024-08935/medical-devices-laboratory-developed-tests'
fda_announcement = 'https://www.fda.gov/news-events/press-announcements/fda-takes-action-aimed-helping-ensure-safety-and-effectiveness-laboratory-developed-tests'
cfr_download = 'https://www.govinfo.gov/app/collection/cfr/2023/'

ASSISTANTS = {
    'asst_xoY5kRvnY3ApUqMNKHuagMhs': {
        'name': '2024 CAP Checklists',
        'description': """Contains the entire contents of the
        custom checklists for the 2024 self-inspection.""",
        'instructions': """Always include the relevant checklist item
        numbers and titles in the response."""
    },
    'asst_NkjEqM2EfJN2d5gh6EiKwOrl': {
        'name': 'FDA Guidance on Lab Developed Tests',
        'description': f"""Contains the <a href="{ldt_rule}"
        target="_blank">full text</a> of the <a
        href="{fda_announcement}" target="_blank">final rule on lab
        developed tests</a> issued by the FDA in April, 2024.""",
    },
    'asst_BLkdkxwulAC4b5gu1UTrF5Sa': {
        'name': '21CFR: Food and Drugs',
        'description': f"""Contains the <a href="{cfr_download}">2023
        annual edition</a> of the Code of Federal regulations (CFR)
        21""",
        'instructions': """Always include the relevant section number
        and titles in the response.""",
    },
    'asst_3jI1Pkurr9lZvJkQ72oROEhb': {
        'name': '42CFR: Public Health',
        'description': f"""Contains the <a href="{cfr_download}">2023
        annual edition</a> of the Code of Federal regulations (CFR) 42
        """,
        'instructions': """Always include the relevant section number
        and titles in the response.""",
    },
}


def get_features(client: OpenAI,
                 context: str,
                 prompt: str,
                 tools: list,
                 model: str = 'gpt-4o-mini'):

    log.info(f'using model {model}')

    messages = [
        {'role': 'user',
         'content': context},
        {'role': 'user',
         'content': prompt},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice='required',
        # tool_choice='auto',
    )

    output = []
    for tool_call in response.choices[0].message.tool_calls:
        output.append(
            json.loads(tool_call.function.arguments))

    return output


def asst_stream_response(client, thread, assistant_id, prompt, instructions=None):
    """Return a sequence of text deltas

    """

    # add the instructions and prompt to the thread
    if instructions:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=instructions,
        )

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant_id,
            event_handler=AssistantEventHandler(),
    ) as stream:
        for s in stream:
            if isinstance(s, ThreadMessageDelta):
                yield s.data.delta.content[0].text.value


if __name__ == "__main__":
    pass
