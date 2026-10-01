import streamlit as st

from agent import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .hero {
        padding: 30px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #0f172a,
            #172554,
            #1e3a8a
        );
        color: white;
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.9;
    }

    .card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.04);
        min-height: 150px;
    }

    .notice {
        padding: 16px;
        border-radius: 14px;
        background: rgba(245,158,11,0.10);
        border: 1px solid rgba(245,158,11,0.25);
    }

    .footer {
        opacity: 0.7;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🩺 HealTrip AI")

    st.caption("Patient Decision Assistant")

    st.divider()

    st.session_state.language = st.selectbox(
        "Language",
        ["English", "Arabic"],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        ),
    )

    st.divider()

    st.markdown("### Capabilities")

    st.markdown(
        """
        ✅ AI Agent

        ✅ Safety Guardrails

        ✅ Function Calling

        ✅ Doctor Search

        ✅ Hospital Search

        ✅ SQLite Database

        ✅ Arabic / English

        ✅ Anti-Hallucination
        """
    )

    st.divider()

    if st.button(
        "🆕 Start New Assessment",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.conversation = []
        st.session_state.pending_prompt = None

        st.rerun()

    st.divider()

    st.caption(
        "Technical prototype.\n\n"
        "Not a diagnostic medical system."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>🩺 HealTrip AI</h1>

        <p>
        Patient Decision Assistant
        </p>

        <p>
        Safety-aware AI navigation with
        database-grounded healthcare provider discovery.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SAFETY NOTICE
# ============================================================

st.markdown(
    """
    <div class="notice">

    ⚠️ <strong>Safety Notice</strong><br><br>

    HealTrip AI is a technical prototype for healthcare
    decision support. It does not diagnose medical conditions
    and does not replace professional medical evaluation.

    If symptoms may require urgent medical attention,
    seek appropriate medical care.

    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")


# ============================================================
# LANDING PAGE
# ============================================================

if not st.session_state.messages:

    st.markdown("## How can HealTrip AI help?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="card">

            <h3>🧭 Care Direction</h3>

            Helps users identify an appropriate
            next healthcare step based on the
            information they provide.

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="card">

            <h3>👨‍⚕️ Specialist Search</h3>

            Uses database tools to find matching
            specialists instead of inventing providers.

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="card">

            <h3>🏥 Hospital Search</h3>

            Searches the prototype hospital database
            using city, specialty, and emergency capability.

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown("### Try a scenario")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🫀 Chest pain",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "I have chest pain and I am not sure "
                "whether I should see a cardiologist "
                "or go to the emergency department."
            )

            st.rerun()

    with col2:

        if st.button(
            "👨‍⚕️ Find a cardiologist",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "I want to find a cardiologist in Riyadh."
            )

            st.rerun()

    with col3:

        if st.button(
            "🏥 Find a hospital",
            use_container_width=True,
        ):

            st.session_state.pending_prompt = (
                "I need a hospital in Riyadh with emergency services."
            )

            st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_prompt = st.chat_input(
    "Describe your situation or ask about a specialist..."
)


if st.session_state.pending_prompt:

    user_prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None


# ============================================================
# AI PROCESSING
# ============================================================

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your request..."):

            try:

                result = run_agent(
                    user_message=user_prompt,
                    conversation=st.session_state.conversation,
                )

                answer = result.get(
                    "answer",
                    "No response was generated.",
                )

                tools_used = result.get(
                    "tools_used",
                    [],
                )

                emergency = result.get(
                    "emergency",
                    False,
                )

                st.markdown(answer)

                if emergency:

                    st.warning(
                        "Safety escalation activated."
                    )

                if tools_used:

                    with st.expander(
                        "🔧 AI Agent Tools Used"
                    ):

                        for tool in tools_used:

                            st.write(
                                f"• `{tool}`"
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
                        "content": user_prompt,
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
                    "Unfortunately, the AI service is currently unavailable."
                )

                with st.expander(
                    "🔍 Technical diagnostics"
                ):

                    st.code(
                        "Error type:\n"
                        + type(error).__name__
                        + "\n\n"
                        + "Error message:\n"
                        + str(error)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">

    HealTrip AI • Safety-aware • Tool-using • Multilingual •
    Database-grounded

    </div>
    """,
    unsafe_allow_html=True,
)
