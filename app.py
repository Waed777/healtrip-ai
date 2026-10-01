import streamlit as st
from agent import run_agent


st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🩺",
    layout="wide",
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []


st.title("🩺 HealTrip AI")

st.subheader("Patient Decision Assistant")

st.write(
    "Safety-aware AI navigation with "
    "database-grounded healthcare provider discovery."
)


st.info(
    "HealTrip AI is a technical prototype. "
    "It does not diagnose medical conditions "
    "and does not replace professional medical care."
)


language = st.selectbox(
    "Language",
    ["English", "العربية"],
)


st.divider()


st.markdown("### Capabilities")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("🤖 AI Agent")
    st.write("🛡️ Safety Guardrails")

with col2:
    st.write("🔧 Function Calling")
    st.write("👨‍⚕️ Doctor Search")

with col3:
    st.write("🏥 Hospital Search")
    st.write("🌐 Arabic / English")


st.divider()


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


user_message = st.chat_input(
    "Describe your situation..."
)


if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.write(user_message)

    with st.chat_message("assistant"):

        try:

            result = run_agent(
                user_message=user_message,
                conversation=st.session_state.conversation,
            )

            answer = result["answer"]

            st.write(answer)

            if result.get("tools_used"):

                st.caption(
                    "Tools used: "
                    + ", ".join(
                        result["tools_used"]
                    )
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.session_state.conversation.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            st.session_state.conversation.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as error:

            st.error(
                "AI service error"
            )

            st.code(
                f"{type(error).__name__}: {error}"
            )


st.divider()

st.caption(
    "HealTrip AI • Technical Prototype • "
    "Not a diagnostic medical system"
)
