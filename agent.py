import json
import os

from openai import OpenAI

from safety import detect_emergency, emergency_response
from tools import TOOL_DEFINITIONS, execute_tool


MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

SYSTEM_PROMPT = """
You are HealTrip AI, a Patient Decision Assistant.

Your job is to help users decide what type of medical next step may be
appropriate based on the information they provide.

You are NOT a doctor.
You MUST NOT diagnose diseases.
You MUST NOT claim certainty about a medical condition.

SAFETY:
- If symptoms suggest a possible emergency, prioritize urgent medical
  evaluation.
- Do not delay emergency care by asking unnecessary questions.
- Do not provide instructions that could replace professional emergency care.

CLARIFICATION:
- Ask concise clarifying questions when important information is missing.
- Useful information may include age, symptoms, duration, severity,
  associated symptoms, and relevant medical context.

TOOLS:
- Use the doctor search tool when the user asks for a specialist or doctor.
- Use the hospital search tool when the user asks for hospital options.
- Use the tools instead of inventing provider information.

ANTI-HALLUCINATION:
- NEVER invent doctors.
- NEVER invent hospitals.
- NEVER invent availability, appointments, prices, ratings, phone numbers,
  addresses, or medical credentials.
- Only mention doctors and hospitals returned by the tools.
- If the database has no matching result, explicitly say that no matching
  provider was found in the prototype database.

LANGUAGE:
- Reply in the user's language.
- Support both Arabic and English.
- Keep responses clear and concise.

DECISION SUPPORT:
When appropriate, structure the answer as:
1. Suggested next step
2. Why
3. What information is still needed
4. Verified provider/hospital options if requested

Always make clear that HealTrip AI is a prototype decision-support system.
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
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    return OpenAI(api_key=api_key)


def detect_language(text):
    arabic_characters = sum(
        1 for character in text
        if "\u0600" <= character <= "\u06ff"
    )

    return "Arabic" if arabic_characters > 3 else "English"


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

    input_items = conversation + [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=input_items,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        parallel_tool_calls=True,
    )

    tools_used = []

    for item in response.output:
        if item.type != "function_call":
            continue

        tools_used.append(item.name)

        try:
            arguments = json.loads(item.arguments)
        except json.JSONDecodeError:
            arguments = {}

        tool_output = execute_tool(
            item.name,
            arguments,
        )

        input_items.append(item)

        input_items.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": tool_output,
            }
        )

    if tools_used:
        final_response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=input_items,
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
