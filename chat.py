import logging
import json

from openai import OpenAI, AssistantEventHandler
from openai.types.beta.assistant_stream_event import ThreadMessageDelta

log = logging.getLogger(__name__)


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
