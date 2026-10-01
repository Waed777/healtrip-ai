import json
import os

from openai import OpenAI

from safety import detect_emergency, emergency_response
from tools import TOOL_DEFINITIONS, execute_tool


MODEL = os.getenv("OPENAI_MODEL", "gpt-5")


SYSTEM_PROMPT = """
You are HealTrip AI, a Patient Decision Assistant.

You help users identify an appropriate next healthcare step.

You are NOT a doctor.
You MUST NOT diagnose diseases.
You MUST NOT claim certainty about a medical condition.

If symptoms may indicate an emergency, prioritize urgent medical evaluation.

Ask concise clarification questions when important information is missing.

Use database tools when the user asks for doctors or hospitals.

Never invent doctors, hospitals, appointments, prices, ratings,
phone numbers, addresses, or availability.

Only mention providers returned by the database tools.

If no provider is found, clearly say that no matching provider
was found in the prototype database.

Respond in the user's language.

Support Arabic and English.

This is a technical prototype and not a diagnostic medical system.
"""


def get_api_key():
    api_key = None

    try:
        import streamlit as st

        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing."
        )

    if not isinstance(api_key, str):
        raise RuntimeError(
            "OPENAI_API_KEY is not a string."
        )

    api_key = api_key.strip()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is empty."
        )

    try:
        api_key.encode("ascii")
    except UnicodeEncodeError:
        raise RuntimeError(
            "OPENAI_API_KEY contains non-ASCII characters. "
            "Create a new API key and paste it directly into "
            "Streamlit Secrets."
        )

    return api_key


def get_client():

    api_key = get_api_key()

    return OpenAI(
        api_key=api_key,
    )


def detect_language(text):

    arabic_count = sum(
        1
        for character in text
        if "\u0600" <= character <= "\u06ff"
    )

    if arabic_count > 3:
        return "Arabic"

    return "English"


def run_agent(
    user_message,
    conversation=None,
):

    language = detect_language(
        user_message
    )

    emergency = detect_emergency(
        user_message
    )

    if emergency["is_emergency"]:

        return {
            "answer": emergency_response(
                language
            ),
            "tools_used": [],
            "emergency": True,
        }

    client = get_client()

    if conversation is None:
        conversation = []

    input_items = []

    for message in conversation:

        input_items.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    input_items.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=input_items,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
    )

    tools_used = []

    tool_outputs = []

    for item in response.output:

        if item.type != "function_call":
            continue

        tools_used.append(
            item.name
        )

        try:
            arguments = json.loads(
                item.arguments
            )
        except Exception:
            arguments = {}

        tool_result = execute_tool(
            item.name,
            arguments,
        )

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": tool_result,
            }
        )

    if tool_outputs:

        follow_up_input = input_items.copy()

        for item in response.output:
            follow_up_input.append(item)

        follow_up_input.extend(
            tool_outputs
        )

        final_response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=follow_up_input,
            tools=TOOL_DEFINITIONS,
        )

        answer = final_response.output_text

    else:

        answer = response.output_text

    return {
        "answer": answer,
        "tools_used": tools_used,
        "emergency": False,
    }
