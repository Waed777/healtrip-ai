import json
import os

from openai import OpenAI

from safety import detect_emergency, emergency_response
from tools import TOOL_DEFINITIONS, execute_tool


MODEL = os.getenv("OPENAI_MODEL", "gpt-5")


SYSTEM_PROMPT = """
You are HealTrip AI, a Patient Decision Assistant.

Your job is to help users identify an appropriate healthcare next step.

You are NOT a doctor.
You MUST NOT diagnose diseases.
You MUST NOT claim certainty about a medical condition.

SAFETY:
- If symptoms may indicate an emergency, prioritize urgent medical evaluation.
- Do not delay emergency care with unnecessary questions.
- Do not replace professional medical care.

CLARIFICATION:
- Ask concise clarifying questions when important information is missing.
- Useful information includes age, symptoms, duration, severity, and associated symptoms.

TOOLS:
- Use search_doctors when the user asks for a doctor or specialist.
- Use search_hospitals when the user asks for hospital options.
- Never invent doctors or hospitals.
- Never invent appointments or availability.

ANTI-HALLUCINATION:
- Only mention doctors and hospitals returned by the database tools.
- If there is no matching result, clearly say that no matching provider was found
  in the prototype database.

LANGUAGE:
- Respond in the user's language.
- Support Arabic and English.

RESPONSE:
When appropriate, structure the response as:
1. Suggested next step
2. Reason
3. Information still needed
4. Verified provider or hospital options

Always remember that HealTrip AI is a prototype decision-support system.
"""


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    return OpenAI(api_key=api_key)


def detect_language(text):
    arabic_count = sum(
        1
        for character in text
        if "\u0600" <= character <= "\u06ff"
    )

    if arabic_count > 3:
        return "Arabic"

    return "English"


def run_agent(user_message, conversation=None):

    language = detect_language(user_message)

    emergency = detect_emergency(user_message)

    if emergency["is_emergency"]:
        return {
            "answer": emergency_response(language),
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

        tools_used.append(item.name)

        try:
            arguments = json.loads(item.arguments)
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

        follow_up_input.extend(tool_outputs)

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
