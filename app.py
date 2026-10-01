```python
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

if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False

if "language" not in st.session_state:
    st.session_state.language = "English"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 28px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 50%,
            #1e3a8a 100%
        );
        color: white;
        margin-bottom: 24px;
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
        margin-bottom: 16px;
        background: rgba(128,128,128,0.04);
    }

    .small-text {
        font-size: 13px;
        opacity: 0.75;
    }

    .success-box {
        padding: 14px;
        border-radius: 12px;
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.25);
    }

    .warning-box {
        padding: 14px;
        border-radius: 12px;
        background: rgba(245,158,11,0.10);
        border: 1px solid rgba(245,158,11,0.25);
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

    language = st.selectbox(
        "Language",
        ["English", "Arabic"],
        index=0 if st.session_state.language == "English" else 1,
    )

    st.session_state.language = language

    st.divider()

    st.markdown("### System capabilities")

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
        st.session_state.assessment_started = False
        st.rerun()

    st.divider()

    st.caption(
        "Prototype for technical evaluation.\n\n"
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
        AI-powered healthcare navigation with
        safety-aware reasoning, database tools,
        and multilingual support.
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
    <div class="warning-box">

    ⚠️ <strong>Safety Notice</strong><br><br>

    HealTrip AI is a technical prototype designed to support
    healthcare decision navigation. It does not diagnose medical
    conditions and does not replace professional medical care.

    If symptoms may require urgent medical attention,
    seek appropriate emergency medical evaluation.

    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")


# ============================================================
# INTRO / QUICK ACTIONS
# ============================================================

if not st.session_state.messages:

    st.markdown("## How can HealTrip AI help?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">

            <h3>🧭 Care Direction</h3>

            Helps identify an appropriate
            next healthcare step based on
            the information provided.

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">

            <h3>👨‍⚕️ Specialist Search</h3>

            Uses database tools to find
            matching specialists instead
            of inventing providers.

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">

            <h3>🏥 Hospital Search</h3>

            Searches the prototype hospital
            database according to location,
            specialty, and emergency capability.

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Try a scenario")

    example_col1, example_col2 = st.columns(2)

    with example_col1:

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

    with example_col2:

        if st.button(
            "👨‍⚕️ Find a cardiologist",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "I want to find a cardiologist in Riyadh."
            )
            st.rerun()

    st.write("")

    st.markdown(
        """
        <div class="small-text">

        Example: You can describe your symptoms,
        ask for a specialist, or ask for hospital options.

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(
        "user" if role == "user" else "assistant"
    ):

        st.markdown(message["content"])


# ============================================================
# PENDING EXAMPLE
# ============================================================

pending_prompt = st.session_state.pop(
    "pending_prompt",
    None,
)


# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Describe your situation or ask about a specialist..."
)


if pending_prompt:
    user_prompt = pending_prompt


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_prompt:

    st.session_state.assessment_started = True

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

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

                # --------------------------------------------
                # DISPLAY RESPONSE
                # --------------------------------------------

                st.markdown(answer)

                # --------------------------------------------
                # SAFETY STATUS
                # --------------------------------------------

                if emergency:

                    st.warning(
                        "Safety escalation activated."
                    )

                # --------------------------------------------
                # TOOL TRANSPARENCY
                # --------------------------------------------

                if tools_used:

                    with st.expander(
                        "🔧 Tools used by AI Agent"
                    ):

                        for tool in tools_used:

                            st.write(
                                f"• `{tool}`"
                            )

                # --------------------------------------------
                # SAVE ASSISTANT MESSAGE
                # --------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                # --------------------------------------------
                # UPDATE CONVERSATION
                # --------------------------------------------

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

                # ============================================
                # USER FRIENDLY ERROR
                # ============================================

                st.error(
                    "Unfortunately, the AI service is currently "
                    "unavailable."
                )

                st.markdown(
                    """
                    Please check the technical diagnostics below.
                    This diagnostic information is displayed
                    temporarily during development.
                    """
                )

                # ============================================
                # REAL ERROR
                # ============================================

                with st.expander(
                    "🔍 Technical diagnostics — click to open"
                ):

                    st.code(
                        f"Error type:\n"
                        f"{type(error).__name__}\n\n"
                        f"Error message:\n"
                        f"{str(error)}"
                    )

                    st.write(
                        "This information does not expose your "
                        "OpenAI API key."
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

footer_col1, footer_col2 = st.columns(2)

with footer_col1:

    st.caption(
        "HealTrip AI • AI-powered healthcare navigation prototype"
    )

with footer_col2:

    st.caption(
        "Safety-aware • Tool-using • Multilingual • Database-grounded"
    )
