import streamlit as st

from agent import run_agent
from database import initialize_database


st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)


initialize_database()


st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .disclaimer {
        background-color: #fff7ed;
        padding: 14px;
        border-radius: 10px;
        border: 1px solid #fed7aa;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.title("🩺 HealTrip AI")

    st.markdown(
        """
        **Patient Decision Assistant**

        This prototype demonstrates:

        - AI Agent
        - Function Calling
        - Provider Search
        - Hospital Search
        - Safety Guardrails
        - SQLite Database
        - Arabic / English support
        """
    )

    st.divider()

    st.subheader("Architecture")

    st.code(
        """
Patient
   ↓
Streamlit UI
   ↓
AI Agent
   ↓
Safety Layer
   ↓
Function Tools
   ↓
SQLite Database
        """,
        language="text",
    )

    st.divider()

    st.caption(
        "Prototype for technical evaluation. "
        "Not a diagnostic medical system."
    )


st.markdown(
    '<div class="main-title">🩺 HealTrip AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Patient Decision Assistant"
    "</div>",
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="disclaimer">
    ⚠️ <b>Safety notice:</b> HealTrip AI does not diagnose medical
    conditions. For severe or worsening symptoms, seek urgent medical care.
    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")


if "messages" not in st.session_state:
    st.session_state.messages = []


if "conversation" not in st.session_state:
    st.session_state.conversation = []


if not st.session_state.messages:
    st.info(
        "Try: “I have chest discomfort and I am not sure "
        "whether I should see a cardiologist.”"
    )


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("tools_used"):
            st.caption(
                "Tools used: "
                + ", ".join(message["tools_used"])
            )


prompt = st.chat_input(
    "Describe your concern..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your request..."):

            try:
                result = run_agent(
                    user_message=prompt,
                    conversation=st.session_state.conversation,
                )

                answer = result["answer"]
                tools_used = result["tools_used"]

            except Exception as error:

                answer = (
                    "I’m sorry, but the AI service is currently "
                    "unavailable. Please try again later.\n\n"
                    f"Technical status: `{type(error).__name__}`"
                )

                tools_used = []

        st.markdown(answer)

        if tools_used:
            st.caption(
                "Verified database tools used: "
                + ", ".join(tools_used)
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "tools_used": tools_used,
        }
    )

    st.session_state.conversation.extend(
        [
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "assistant",
                "content": answer,
            },
        ]
    )
