import json
import os

from openai import OpenAI

from safety import (
    detect_emergency,
    emergency_response,
)

from tools import (
    TOOL_DEFINITIONS,
    execute_tool,
)


DEFAULT_MODEL = "gpt-4o-mini"


SYSTEM_PROMPT = """
You are HealTrip AI, a healthcare navigation assistant.

You are not a doctor.

You must not diagnose diseases.

You help users understand possible next healthcare steps.

SAFETY:

If the user describes potentially urgent symptoms,
prioritize urgent medical evaluation.

Do not delay emergency care by asking unnecessary questions.

CLARIFICATION:

When important information is missing,
ask concise questions such as age, duration,
severity, and associated symptoms.

TOOLS:

Use search_doctors when the user asks for a doctor or specialist.

Use search_hospitals when the user asks for hospital options.

Never invent doctors.

Never invent hospitals.

Never invent appointments.

Never invent availability.

Never invent prices.

Never invent ratings.

Never invent phone numbers.

Only mention provider information returned by the tools.

The database is prototype/demo data.

If no matching provider exists,
say that no matching provider was found
in the HealTrip prototype database.

LANGUAGE:

Respond in the user's language.

Support Arabic and English.

STYLE:

Be concise.

Be calm.

Be structured.

When appropriate use:

Suggested next step
Reason
Questions
Available options

MEDICAL SAFETY:

This is decision support only.

It is not a diagnosis.

Do not claim certainty about a medical condition.
"""


def get_api_key():

    api_key = None

    try:

        import streamlit as st

        api_key = st.secrets.get(
            "OPENAI_API_KEY"
        )

    except Exception:

        api_key = None

    if not api_key:

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

    if not api_key:

        return None

    api_key = str(api_key)

    api_key = api_key.strip()

    if not api_key:

        return None

    return api_key


def get_model():

    try:

        import streamlit as st

        model = st.secrets.get(
            "OPENAI_MODEL"
        )

        if model:
            return str(model).strip()

    except Exception:

        pass

    model = os.getenv(
        "OPENAI_MODEL",
        DEFAULT_MODEL,
    )

    return model.strip()


def detect_language(text):

    arabic_count = sum(
        1
        for character in text
        if "\u0600" <= character <= "\u06ff"
    )

    if arabic_count >= 2:
        return "Arabic"

    return "English"


def local_fallback(
    user_message,
    language,
):

    text = user_message.lower()

    if language == "Arabic":

        if (
            "طبيب" in text
            or "دكتور" in text
            or "طبيبة" in text
        ):

            return """
### 👨‍⚕️ البحث عن طبيب

أستطيع مساعدتك في البحث داخل قاعدة بيانات HealTrip التجريبية.

جرّبي مثلاً:

**"أريد طبيب قلب في الرياض"**

أو:

**"أريد طبيب باطنية في الرياض"**

> البيانات المعروضة في هذا البروتوتايب تجريبية وليست نظام حجز حقيقي.
"""

        if "مستشفى" in text:

            return """
### 🏥 البحث عن مستشفى

أستطيع البحث داخل قاعدة بيانات المستشفيات التجريبية.

يمكنك تحديد:

- المدينة
- التخصص
- هل تحتاجين إلى طوارئ

مثال:

**"أريد مستشفى في الرياض فيه طوارئ."**
"""

        return """
### 🤖 HealTrip AI

أستطيع مساعدتك في تحديد الخطوة الصحية التالية.

يمكنك أن تخبريني:

- ما الأعراض؟
- منذ متى بدأت؟
- هل هي شديدة؟
- العمر؟
- هل توجد أعراض أخرى؟

وإذا كنت تبحثين عن طبيب أو مستشفى، اذكري المدينة والتخصص.
"""

    if (
        "doctor" in text
        or "specialist" in text
    ):

        return """
### 👨‍⚕️ Doctor Search

I can search the HealTrip prototype provider database.

Try:

**"Find a cardiologist in Riyadh."**

or:

**"Find an internal medicine doctor in Riyadh."**

The displayed providers are demo records, not live appointment data.
"""

    if "hospital" in text:

        return """
### 🏥 Hospital Search

I can search the prototype hospital database.

You can specify:

- City
- Specialty
- Emergency requirement

Example:

**"Find a hospital in Riyadh with emergency services."**
"""

    return """
### 🤖 HealTrip AI

I can help you navigate the next healthcare step.

Tell me:

- Your symptoms
- How long they have been present
- Severity
- Your age
- Any associated symptoms

You can also ask me to search for a doctor or hospital.
"""


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
            "mode": "safety",
        }

    api_key = get_api_key()

    if not api_key:

        return {
            "answer": local_fallback(
                user_message,
                language,
            ),
            "tools_used": [],
            "emergency": False,
            "mode": "local_fallback",
            "error": "OPENAI_API_KEY is not configured.",
        }

    try:

        client = OpenAI(
            api_key=api_key
        )

        model = get_model()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        if conversation:

            for message in conversation[-10:]:

                if message.get("role") in [
                    "user",
                    "assistant",
                ]:

                    messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                    )

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        tools_used = []

        if assistant_message.tool_calls:

            messages.append(
                assistant_message.model_dump(
                    exclude_none=True
                )
            )

            for tool_call in assistant_message.tool_calls:

                function_name = (
                    tool_call.function.name
                )

                tools_used.append(
                    function_name
                )

                try:

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                except Exception:

                    arguments = {}

                tool_result = execute_tool(
                    function_name,
                    arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )

            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
            )

            answer = (
                final_response.choices[0]
                .message
                .content
            )

        else:

            answer = assistant_message.content

        if not answer:

            answer = local_fallback(
                user_message,
                language,
            )

        return {
            "answer": answer,
            "tools_used": tools_used,
            "emergency": False,
            "mode": "openai",
        }

    except Exception as error:

        fallback = local_fallback(
            user_message,
            language,
        )

        return {
            "answer": fallback,
            "tools_used": [],
            "emergency": False,
            "mode": "fallback",
            "error": (
                f"{type(error).__name__}: "
                f"{str(error)}"
            ),
        }
