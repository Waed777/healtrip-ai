import streamlit as st

from database import (
    initialize_database,
    search_doctors,
    search_hospitals,
)

from agent import run_agent


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


initialize_database()


# ============================================================
# SESSION
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at top right,
            rgba(37, 99, 235, 0.12),
            transparent 35%
        ),
        #07111f;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.hero {
    padding: 36px;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            #0b1220 0%,
            #111c36 55%,
            #123b73 100%
        );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin: 0;
}

.hero-subtitle {
    color: #b9c7dd;
    font-size: 19px;
    margin-top: 8px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(59,130,246,0.16);
    border: 1px solid rgba(96,165,250,0.25);
    color: #bfdbfe;
    font-size: 13px;
    margin-bottom: 14px;
}

.feature-card {
    padding: 22px;
    min-height: 145px;
    border-radius: 20px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(148,163,184,0.14);
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
}

.feature-text {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
}

.robot {
    font-size: 80px;
    text-align: center;
    padding: 15px;
}

.robot-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
}

.robot-text {
    text-align: center;
    color: #94a3b8;
}

.safety {
    padding: 18px;
    border-radius: 18px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.20);
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-top: 25px;
}

.small-muted {
    color: #94a3b8;
    font-size: 13px;
}

.provider-card {
    padding: 18px;
    border-radius: 16px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(148,163,184,0.14);
    margin-bottom: 12px;
}

.arch {
    padding: 22px;
    border-radius: 18px;
    background: #0b1220;
    border: 1px solid rgba(96,165,250,0.18);
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 HealTrip AI")

    st.caption(
        "Patient Decision Assistant"
    )

    st.divider()

    language = st.radio(
        "Language",
        ["English", "العربية"],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        ),
    )

    st.session_state.language = (
        "Arabic"
        if language == "العربية"
        else "English"
    )

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "🤖 AI Assistant",
            "🧭 Care Path",
            "👨‍⚕️ Providers",
            "📋 Patient Summary",
            "🏗️ Architecture",
        ],
    )

    st.divider()

    if st.button(
        "🆕 New Assessment",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.conversation = []
        st.session_state.last_result = None

        st.rerun()

    st.divider()

    st.caption(
        "Prototype database\n"
        "No live appointments\n"
        "Not a diagnostic system"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-badge">
AI HEALTHCARE NAVIGATION
</div>

<div class="hero-title">
🤖 HealTrip AI
</div>

<div class="hero-subtitle">
Patient Decision Assistant
</div>

<p style="color:#cbd5e1; max-width:800px;">
A safety-aware AI assistant designed to help users
navigate their next healthcare step using structured
reasoning, database tools, and multilingual interaction.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# ASSISTANT PAGE
# ============================================================

if page == "🤖 AI Assistant":

    st.markdown(
        """
<div class="safety">

⚠️ <strong>Safety Notice</strong><br><br>

HealTrip AI is a technical prototype.
It does not diagnose medical conditions and
does not replace professional medical care.

If symptoms may require urgent evaluation,
seek appropriate medical attention.

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns(
        [1.7, 1]
    )

    with left:

        st.markdown(
            '<div class="section-title">AI Patient Assistant</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.messages:

            st.info(
                "Tell HealTrip AI what you need. "
                "You can describe symptoms, ask for a specialist, "
                "or search for a hospital."
            )

            quick1, quick2, quick3 = st.columns(3)

            with quick1:

                if st.button(
                    "🫀 Chest pain",
                    use_container_width=True,
                ):

                    st.session_state.quick_prompt = (
                        "I have chest pain and I am not sure "
                        "what my next healthcare step should be."
                    )

                    st.rerun()

            with quick2:

                if st.button(
                    "👨‍⚕️ Cardiologist",
                    use_container_width=True,
                ):

                    st.session_state.quick_prompt = (
                        "I want a cardiologist in Riyadh."
                    )

                    st.rerun()

            with quick3:

                if st.button(
                    "🏥 Hospital",
                    use_container_width=True,
                ):

                    st.session_state.quick_prompt = (
                        "Find hospitals in Riyadh with emergency services."
                    )

                    st.rerun()

        for message in st.session_state.messages:

            avatar = (
                "🤖"
                if message["role"] == "assistant"
                else "👤"
            )

            with st.chat_message(
                message["role"],
                avatar=avatar,
            ):

                st.markdown(
                    message["content"]
                )

        prompt = st.chat_input(
            "Describe your situation..."
        )

        if "quick_prompt" in st.session_state:

            prompt = st.session_state.pop(
                "quick_prompt"
            )

        if prompt:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            with st.chat_message(
                "user",
                avatar="👤",
            ):

                st.markdown(prompt)

            with st.chat_message(
                "assistant",
                avatar="🤖",
            ):

                with st.spinner(
                    "HealTrip AI is thinking..."
                ):

                    result = run_agent(
                        user_message=prompt,
                        conversation=st.session_state.conversation,
                    )

                answer = result["answer"]

                st.markdown(answer)

                if result.get("tools_used"):

                    with st.expander(
                        "🔧 Agent Tool Trace"
                    ):

                        for tool in result[
                            "tools_used"
                        ]:

                            st.success(
                                f"Executed: {tool}"
                            )

                if result.get("mode") == "fallback":

                    with st.expander(
                        "Developer diagnostics"
                    ):

                        st.code(
                            result.get(
                                "error",
                                "Unknown error",
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
                        "content": prompt,
                    }
                )

                st.session_state.conversation.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.session_state.last_result = result

    with right:

        st.markdown(
            """
<div class="robot">
🤖
</div>

<div class="robot-title">
HealTrip Intelligence
</div>

<div class="robot-text">
Reason → Check Safety → Use Tools → Respond
</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
🧠 AI Reasoning
</div>

<div class="feature-text">
The assistant interprets the user's request
and determines whether additional information
or a database tool is required.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
🛡️ Safety Layer
</div>

<div class="feature-text">
Potential urgent symptoms are checked before
normal provider recommendations.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
🔒 Grounded Results
</div>

<div class="feature-text">
Provider information comes from the prototype
database rather than being invented by the model.
</div>

</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# CARE PATH
# ============================================================

elif page == "🧭 Care Path":

    st.markdown(
        '<div class="section-title">🧭 Care Path</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "A transparent view of how HealTrip AI approaches a request."
    )

    steps = [
        (
            "01",
            "Understand",
            "Interpret the user's concern and context.",
        ),
        (
            "02",
            "Safety Check",
            "Identify signals that may require urgent evaluation.",
        ),
        (
            "03",
            "Clarify",
            "Ask for important missing information.",
        ),
        (
            "04",
            "Choose Tool",
            "Search the appropriate provider or hospital data.",
        ),
        (
            "05",
            "Ground",
            "Use returned database records only.",
        ),
        (
            "06",
            "Respond",
            "Provide a clear next-step explanation.",
        ),
    ]

    for number, title, description in steps:

        c1, c2 = st.columns(
            [0.15, 0.85]
        )

        with c1:
            st.markdown(
                f"### {number}"
            )

        with c2:
            st.markdown(
                f"### {title}"
            )
            st.write(description)

        st.divider()


# ============================================================
# PROVIDERS
# ============================================================

elif page == "👨‍⚕️ Providers":

    st.markdown(
        '<div class="section-title">👨‍⚕️ Provider Search</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Demo database only. These records are synthetic prototype data. "
        "They do not represent live availability or real-world verification."
    )

    tab1, tab2 = st.tabs(
        [
            "👨‍⚕️ Doctors",
            "🏥 Hospitals",
        ]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            specialty = st.selectbox(
                "Specialty",
                [
                    "Any",
                    "Cardiology",
                    "Internal Medicine",
                    "Pulmonology",
                ],
            )

        with col2:

            city = st.selectbox(
                "City",
                [
                    "Any",
                    "Riyadh",
                    "Jeddah",
                ],
            )

        doctors = search_doctors(
            specialty=(
                None
                if specialty == "Any"
                else specialty
            ),
            city=(
                None
                if city == "Any"
                else city
            ),
        )

        st.write(
            f"**{len(doctors)} provider records found**"
        )

        for doctor in doctors:

            st.markdown(
                f"""
<div class="provider-card">

### 👨‍⚕️ {doctor["name"]}

**Specialty:** {doctor["specialty"]}

**Hospital:** {doctor["hospital"]}

**Location:** {doctor["city"]}, {doctor["country"]}

**Languages:** {doctor["languages"]}

</div>
""",
                unsafe_allow_html=True,
            )

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            hospital_city = st.selectbox(
                "City",
                [
                    "Any",
                    "Riyadh",
                    "Jeddah",
                ],
                key="hospital_city",
            )

        with col2:

            emergency_only = st.checkbox(
                "Emergency capability only"
            )

        hospitals = search_hospitals(
            city=(
                None
                if hospital_city == "Any"
                else hospital_city
            ),
            emergency_only=emergency_only,
        )

        st.write(
            f"**{len(hospitals)} hospital records found**"
        )

        for hospital in hospitals:

            emergency_status = (
                "Available"
                if hospital["emergency_available"]
                else "Not listed"
            )

            st.markdown(
                f"""
<div class="provider-card">

### 🏥 {hospital["name"]}

**Location:** {hospital["city"]}, {hospital["country"]}

**Specialties:** {hospital["specialties"]}

**Emergency capability in prototype data:** {emergency_status}

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# PATIENT SUMMARY
# ============================================================

elif page == "📋 Patient Summary":

    st.markdown(
        '<div class="section-title">📋 Patient Summary</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:

        st.info(
            "Start a conversation with HealTrip AI first."
        )

    else:

        user_messages = [
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "user"
        ]

        assistant_messages = [
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "assistant"
        ]

        st.markdown(
            "### 🧑‍⚕️ Conversation Overview"
        )

        if user_messages:

            st.markdown(
                "**Patient concern**"
            )

            st.write(
                user_messages[-1]
            )

        if assistant_messages:

            st.markdown(
                "**Latest assistant guidance**"
            )

            st.write(
                assistant_messages[-1]
            )

        st.divider()

        st.markdown(
            "### 🛡️ Safety"
        )

        st.info(
            "This summary is generated from the conversation "
            "and is not a medical record."
        )


# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "🏗️ Architecture":

    st.markdown(
        '<div class="section-title">🏗️ System Architecture</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="arch">

<pre>
Patient
   |
   v
Streamlit UI
   |
   v
Safety Layer
   |
   v
AI Agent
   |
   +-----------------------+
   |                       |
   v                       v
Doctor Tool           Hospital Tool
   |                       |
   +-----------+-----------+
               |
               v
         SQLite Database
               |
               v
        Grounded Results
               |
               v
         AI Response
</pre>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown("### Engineering principles")

    principles = [
        "Safety-first routing",
        "Tool-based provider discovery",
        "Database-grounded responses",
        "No invented providers",
        "No invented availability",
        "Multilingual interaction",
        "Session-based conversation memory",
        "Graceful AI fallback",
        "Clear prototype boundaries",
    ]

    for item in principles:

        st.write(
            f"✓ {item}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "HealTrip AI • Safety-aware • Tool-using • "
    "Multilingual • Database-grounded • Prototype"
)
