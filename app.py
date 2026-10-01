import streamlit as st

from agent import run_agent
from database import initialize_database


st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


initialize_database()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False


# ---------------------------------------------------------
# LANGUAGE
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <h1>🩺 HealTrip AI</h1>
            <p>Patient Decision Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    language = st.radio(
        "Language",
        ["English", "العربية"],
        index=0 if st.session_state.language == "English" else 1,
    )

    if language == "العربية":
        st.session_state.language = "Arabic"
    else:
        st.session_state.language = "English"

    st.divider()

    st.subheader(
        "Patient Assessment"
        if st.session_state.language == "English"
        else "التقييم الصحي"
    )

    st.markdown(
        """
        <div style="
            padding:12px;
            border-radius:10px;
            border:1px solid #d1d5db;
        ">
        🟢 <b>AI Decision Support</b><br>
        🟢 Safety Screening<br>
        🟢 Verified Provider Search<br>
        🟢 Hospital Search<br>
        🟢 Arabic / English
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button(
        "🔄 New Assessment",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.conversation = []
        st.session_state.assessment_started = False
        st.rerun()

    st.divider()

    st.caption(
        "HealTrip AI is a prototype decision-support system. "
        "It does not diagnose medical conditions."
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div style="
        padding:28px;
        border-radius:18px;
        background:linear-gradient(
            135deg,
            #0f172a,
            #1e3a5f
        );
        color:white;
        margin-bottom:25px;
    ">
        <h1 style="margin:0;">
            🩺 HealTrip AI
        </h1>
        <p style="font-size:20px;margin-top:8px;">
            Intelligent Patient Decision Assistant
        </p>
        <p style="opacity:0.85;">
            From symptoms to a safer next step.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# QUICK ACTIONS
# ---------------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        "### How can HealTrip AI help?"
        if st.session_state.language == "English"
        else "### كيف يمكن لـ HealTrip AI مساعدتك؟"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "🚨 **Urgent symptoms**\n\n"
            "Screen symptoms that may require urgent evaluation."
        )

    with col2:
        st.info(
            "🩺 **Find a specialist**\n\n"
            "Search verified doctors by specialty and city."
        )

    with col3:
        st.info(
            "🏥 **Find a hospital**\n\n"
            "Search hospitals using the verified prototype database."
        )

    st.divider()

    st.markdown(
        "### Try a scenario"
        if st.session_state.language == "English"
        else "### جرّبي سيناريو"
    )

    examples = [
        "I have chest discomfort and I am not sure what I should do.",
        "I want to see a cardiologist in Riyadh.",
        "I need a hospital in Riyadh with emergency services.",
        "أريد طبيب قلب في الرياض.",
    ]

    selected_example = st.selectbox(
        "Example",
        examples,
        label_visibility="collapsed",
    )

    if st.button(
        "Use this scenario",
        type="primary",
    ):
        st.session_state.pending_prompt = selected_example
        st.rerun()


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("tools_used"):

            st.caption(
                "🔧 Verified tools: "
                + ", ".join(
                    message["tools_used"]
                )
            )


# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------

prompt = st.chat_input(
    "Describe your concern..."
    if st.session_state.language == "English"
    else "اكتب ما تشعر به..."
)


if "pending_prompt" in st.session_state:

    prompt = st.session_state.pending_prompt

    del st.session_state.pending_prompt


# ---------------------------------------------------------
# AGENT EXECUTION
# ---------------------------------------------------------

if prompt:

    st.session_state.assessment_started = True

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing your request..."
            if st.session_state.language == "English"
            else "جارٍ تحليل طلبك..."
        ):

            try:

                result = run_agent(
                    user_message=prompt,
                    conversation=st.session_state.conversation,
                )

                answer = result["answer"]

                tools_used = result[
                    "tools_used"
                ]

                emergency = result[
                    "emergency"
                ]

            except Exception:

                answer = (
                    "The AI service is temporarily unavailable. "
                    "Please try again shortly."
                    if st.session_state.language == "English"
                    else
                    "خدمة الذكاء الاصطناعي غير متاحة مؤقتًا. "
                    "يرجى المحاولة مرة أخرى."
                )

                tools_used = []

                emergency = False

        if emergency:

            st.error(answer)

        else:

            st.markdown(answer)

        if tools_used:

            st.caption(
                "🔧 Verified tools used: "
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


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "HealTrip AI • AI-powered healthcare decision support prototype • "
    "Not a medical diagnosis system"
)
