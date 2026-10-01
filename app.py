import streamlit as st

from database import initialize_database, search_doctors, search_hospitals
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
# SESSION STATE
# ============================================================

defaults = {
    "messages": [],
    "conversation": [],
    "language": "English",
    "last_result": None,
    "page": "assistant",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


ARABIC = st.session_state.language == "Arabic"


# ============================================================
# TRANSLATIONS
# ============================================================

TEXT = {
    "English": {
        "language": "Language",
        "navigation": "NAVIGATION",
        "assistant": "🤖 AI Assistant",
        "care": "🧭 Care Path",
        "providers": "👨‍⚕️ Providers",
        "summary": "📋 Patient Summary",
        "architecture": "🏗️ Architecture",
        "new": "＋ New Assessment",
        "online": "AI ONLINE",
        "badge": "AI HEALTHCARE NAVIGATION",
        "title": "HealTrip AI",
        "subtitle": "Patient Decision Assistant",
        "hero": (
            "A safety-aware AI assistant for navigating the next "
            "healthcare step through reasoning, safety checks, "
            "database tools, and grounded provider discovery."
        ),
        "safety": "Safety Notice",
        "safety_text": (
            "HealTrip AI is a technical prototype. It does not "
            "diagnose medical conditions and does not replace "
            "professional medical care."
        ),
        "assistant_title": "AI Patient Assistant",
        "assistant_intro": (
            "Describe your situation, ask for a specialist, "
            "or search for a hospital."
        ),
        "chest": "🫀 Chest Pain",
        "cardiologist": "👨‍⚕️ Cardiologist",
        "hospital": "🏥 Hospital Search",
        "placeholder": "Describe your situation...",
        "thinking": "Analyzing your request...",
        "tools": "🔧 Agent Tool Trace",
        "diagnostics": "Developer Diagnostics",
        "intelligence": "HealTrip Intelligence",
        "intelligence_sub": "Reason  •  Safety  •  Tools  •  Grounding",
        "reasoning": "AI Reasoning",
        "reasoning_text": (
            "Interprets the user's request and decides whether "
            "clarification or a database tool is required."
        ),
        "guardrails": "Safety Guardrails",
        "guardrails_text": (
            "Potentially urgent symptoms are checked before "
            "normal provider recommendations."
        ),
        "grounded": "Database Grounding",
        "grounded_text": (
            "Provider information is returned from the prototype "
            "database instead of being invented by the model."
        ),
        "care_title": "Care Path",
        "care_intro": (
            "A transparent view of the decision flow used by HealTrip AI."
        ),
        "understand": "Understand",
        "understand_text": "Interpret the user's concern and context.",
        "check": "Safety Check",
        "check_text": "Check for signals that may require urgent evaluation.",
        "clarify": "Clarify",
        "clarify_text": "Ask for important missing information.",
        "tool": "Choose Tool",
        "tool_text": "Search the appropriate provider or hospital data.",
        "ground": "Ground",
        "ground_text": "Use returned database records only.",
        "respond": "Respond",
        "respond_text": "Provide a clear next-step explanation.",
        "providers_title": "Provider Intelligence",
        "demo": (
            "Synthetic prototype data only. These records do not "
            "represent live availability or real-world verification."
        ),
        "doctors": "Doctors",
        "hospitals": "Hospitals",
        "specialty": "Specialty",
        "city": "City",
        "any": "Any",
        "emergency": "Emergency capability only",
        "records": "records found",
        "location": "Location",
        "languages": "Languages",
        "summary_title": "Patient Summary",
        "start": "Start a conversation with HealTrip AI first.",
        "concern": "Patient Concern",
        "guidance": "Latest AI Guidance",
        "not_record": "This is a conversation summary, not a medical record.",
        "architecture_title": "System Architecture",
        "principles": "Engineering Principles",
        "footer": (
            "HealTrip AI • Safety-aware • Tool-using • "
            "Multilingual • Database-grounded • Prototype"
        ),
        "available": "Available",
        "not_listed": "Not listed",
    },

    "Arabic": {
        "language": "اللغة",
        "navigation": "التنقل",
        "assistant": "🤖 المساعد الذكي",
        "care": "🧭 مسار الرعاية",
        "providers": "👨‍⚕️ الأطباء والمستشفيات",
        "summary": "📋 ملخص الحالة",
        "architecture": "🏗️ بنية النظام",
        "new": "＋ تقييم جديد",
        "online": "الذكاء الاصطناعي متصل",
        "badge": "منصة ذكية للتنقل في الرعاية الصحية",
        "title": "HealTrip AI",
        "subtitle": "مساعد اتخاذ القرار الصحي",
        "hero": (
            "مساعد ذكي وآمن يساعد المستخدم على تحديد الخطوة الصحية "
            "التالية من خلال التحليل، وفحص السلامة، وأدوات البحث، "
            "والاعتماد على بيانات منظمة."
        ),
        "safety": "تنبيه السلامة",
        "safety_text": (
            "HealTrip AI نموذج تقني تجريبي. لا يقوم بتشخيص الحالات "
            "الطبية ولا يحل محل الطبيب أو خدمات الرعاية الصحية."
        ),
        "assistant_title": "المساعد الصحي الذكي",
        "assistant_intro": (
            "صف حالتك، اطلب طبيبًا متخصصًا، أو ابحث عن مستشفى."
        ),
        "chest": "🫀 ألم في الصدر",
        "cardiologist": "👨‍⚕️ طبيب قلب",
        "hospital": "🏥 البحث عن مستشفى",
        "placeholder": "اكتب حالتك أو سؤالك...",
        "thinking": "جاري تحليل طلبك...",
        "tools": "🔧 سجل استخدام الأدوات",
        "diagnostics": "تشخيص للمطور",
        "intelligence": "ذكاء HealTrip",
        "intelligence_sub": "تحليل • سلامة • أدوات • بيانات",
        "reasoning": "التحليل الذكي",
        "reasoning_text": (
            "يفهم المساعد الطلب ويحدد ما إذا كان يحتاج إلى "
            "استيضاح أو استخدام أداة من قاعدة البيانات."
        ),
        "guardrails": "حواجز السلامة",
        "guardrails_text": (
            "يتم فحص المؤشرات التي قد تتطلب رعاية عاجلة قبل "
            "تقديم توصيات عادية."
        ),
        "grounded": "الاعتماد على البيانات",
        "grounded_text": (
            "معلومات الأطباء والمستشفيات تأتي من قاعدة البيانات "
            "التجريبية بدل اختلاقها بواسطة النموذج."
        ),
        "care_title": "مسار الرعاية",
        "care_intro": "عرض شفاف لطريقة اتخاذ القرار داخل HealTrip AI.",
        "understand": "الفهم",
        "understand_text": "فهم المشكلة والسياق.",
        "check": "فحص السلامة",
        "check_text": "البحث عن مؤشرات قد تتطلب تقييمًا عاجلًا.",
        "clarify": "الاستيضاح",
        "clarify_text": "طرح المعلومات المهمة الناقصة.",
        "tool": "اختيار الأداة",
        "tool_text": "البحث في بيانات الأطباء أو المستشفيات.",
        "ground": "الاعتماد على البيانات",
        "ground_text": "استخدام السجلات التي أعادتها قاعدة البيانات فقط.",
        "respond": "الاستجابة",
        "respond_text": "تقديم شرح واضح للخطوة التالية.",
        "providers_title": "ذكاء مقدمي الرعاية",
        "demo": (
            "بيانات تجريبية افتراضية فقط. لا تمثل هذه السجلات "
            "مواعيد مباشرة أو تحققًا من مقدمي الخدمة في العالم الحقيقي."
        ),
        "doctors": "الأطباء",
        "hospitals": "المستشفيات",
        "specialty": "التخصص",
        "city": "المدينة",
        "any": "الكل",
        "emergency": "طوارئ فقط",
        "records": "سجل موجود",
        "location": "الموقع",
        "languages": "اللغات",
        "summary_title": "ملخص الحالة",
        "start": "ابدأ محادثة مع HealTrip AI أولًا.",
        "concern": "مشكلة المستخدم",
        "guidance": "آخر توجيه من الذكاء الاصطناعي",
        "not_record": "هذا ملخص للمحادثة وليس سجلًا طبيًا.",
        "architecture_title": "بنية النظام",
        "principles": "المبادئ الهندسية",
        "footer": (
            "HealTrip AI • آمن • يعتمد على الأدوات • "
            "متعدد اللغات • يعتمد على البيانات • نموذج تجريبي"
        ),
        "available": "متاحة",
        "not_listed": "غير مذكورة",
    },
}


def t(key):
    return TEXT[st.session_state.language][key]


# ============================================================
# PREMIUM DARK DESIGN
# ============================================================

direction = "rtl" if ARABIC else "ltr"
align = "right" if ARABIC else "left"

st.markdown(
    f"""
<style>

/* =========================
   GLOBAL
========================= */

html, body, [class*="css"] {{
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}}

.stApp {{
    background: #020617 !important;
    color: #f8fafc !important;
}}

[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(37, 99, 235, 0.18),
            transparent 24%
        ),
        radial-gradient(
            circle at 5% 75%,
            rgba(14, 165, 233, 0.08),
            transparent 25%
        ),
        #020617 !important;
}}

[data-testid="stHeader"] {{
    background: rgba(2, 6, 23, 0.92) !important;
}}

[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            #030712 0%,
            #07111f 100%
        ) !important;
    border-right: 1px solid #172554 !important;
}}

[data-testid="stSidebar"] * {{
    color: #f8fafc !important;
}}

.block-container {{
    max-width: 1280px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: #ffffff !important;
}}

p, li, label {{
    color: #e2e8f0 !important;
}}

[data-testid="stMarkdownContainer"] {{
    direction: {direction};
    text-align: {align};
}}

/* =========================
   HERO
========================= */

.hero {{
    position: relative;
    overflow: hidden;
    padding: 48px;
    border-radius: 30px;
    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(59,130,246,0.22),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020617 0%,
            #071225 50%,
            #0b1f3a 100%
        );
    border: 1px solid rgba(96,165,250,0.22);
    box-shadow:
        0 30px 80px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.05);
    direction: {direction};
    text-align: {align};
}}

.hero::after {{
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -100px;
    top: -100px;
    border-radius: 50%;
    background: rgba(37,99,235,0.15);
    filter: blur(50px);
}}

.badge {{
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(37,99,235,0.12);
    border: 1px solid rgba(96,165,250,0.30);
    color: #93c5fd !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}}

.hero-title {{
    position: relative;
    z-index: 1;
    margin-top: 18px;
    font-size: 56px;
    line-height: 1.05;
    font-weight: 900;
    color: #ffffff !important;
}}

.hero-subtitle {{
    position: relative;
    z-index: 1;
    margin-top: 10px;
    font-size: 23px;
    color: #93c5fd !important;
    font-weight: 600;
}}

.hero-description {{
    position: relative;
    z-index: 1;
    max-width: 850px;
    margin-top: 18px;
    font-size: 16px;
    line-height: 1.8;
    color: #cbd5e1 !important;
}}

/* =========================
   STATUS
========================= */

.status {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.20);
    color: #6ee7b7 !important;
    font-size: 12px;
    font-weight: 700;
}}

.status-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 12px #22c55e;
}}

/* =========================
   CARDS
========================= */

.glass {{
    padding: 22px;
    border-radius: 20px;
    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.92),
            rgba(7,17,31,0.88)
        );
    border: 1px solid rgba(71,85,105,0.35);
    box-shadow:
        0 15px 40px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.025);
}}

.card-title {{
    color: #ffffff !important;
    font-size: 18px;
    font-weight: 800;
}}

.card-text {{
    color: #94a3b8 !important;
    font-size: 14px;
    line-height: 1.7;
}}

/* =========================
   AI CORE
========================= */

.ai-core {{
    text-align: center;
    padding: 25px 15px;
}}

.ai-orb {{
    width: 150px;
    height: 150px;
    margin: 0 auto 20px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 70px;
    background:
        radial-gradient(
            circle,
            #172554 0%,
            #0b1730 45%,
            #020617 75%
        );
    border: 1px solid rgba(96,165,250,0.45);
    box-shadow:
        0 0 30px rgba(37,99,235,0.35),
        0 0 80px rgba(37,99,235,0.18),
        inset 0 0 30px rgba(59,130,246,0.10);
}}

.ai-title {{
    color: #ffffff !important;
    font-size: 22px;
    font-weight: 800;
}}

.ai-subtitle {{
    color: #64748b !important;
    font-size: 13px;
    margin-top: 5px;
}}

/* =========================
   SAFETY
========================= */

.safety {{
    padding: 20px;
    border-radius: 18px;
    background:
        linear-gradient(
            135deg,
            rgba(120,53,15,0.22),
            rgba(69,26,3,0.15)
        );
    border: 1px solid rgba(245,158,11,0.22);
    color: #f8fafc !important;
}}

.safety * {{
    color: #f8fafc !important;
}}

/* =========================
   STREAMLIT INPUTS
========================= */

.stButton > button {{
    background: #0b1220 !important;
    color: #f8fafc !important;
    border: 1px solid #263750 !important;
    border-radius: 12px !important;
    min-height: 43px;
    font-weight: 600;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    background: #10213a !important;
    border-color: #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59,130,246,0.15);
}}

[data-testid="stChatMessage"] {{
    background: rgba(10,18,32,0.90) !important;
    border: 1px solid #1e293b !important;
    border-radius: 18px !important;
}}

[data-testid="stChatMessage"] * {{
    color: #f8fafc !important;
}}

[data-testid="stChatInput"] {{
    background: #080f1c !important;
}}

[data-testid="stChatInput"] textarea {{
    background: #080f1c !important;
    color: #ffffff !important;
    border-color: #263750 !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: #64748b !important;
}}

.stSelectbox > div > div,
[data-baseweb="select"] {{
    background: #0b1220 !important;
    color: #ffffff !important;
}}

[data-baseweb="select"] * {{
    color: #ffffff !important;
}}

[role="option"] {{
    background: #0b1220 !important;
    color: #ffffff !important;
}}

[role="option"]:hover {{
    background: #172554 !important;
}}

[data-testid="stExpander"] {{
    background: #080f1c !important;
    border: 1px solid #1e293b !important;
    border-radius: 14px !important;
}}

[data-testid="stExpander"] * {{
    color: #f8fafc !important;
}}

[data-testid="stAlert"] {{
    background: #0b1424 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    color: #94a3b8 !important;
    background: #080f1c !important;
    border-radius: 10px !important;
}}

.stTabs [aria-selected="true"] {{
    color: #ffffff !important;
    background: #1d4ed8 !important;
}}

/* =========================
   PROVIDER
========================= */

.provider {{
    padding: 20px;
    margin-bottom: 14px;
    border-radius: 18px;
    background: #080f1c;
    border: 1px solid #1e293b;
    transition: all 0.2s ease;
}}

.provider:hover {{
    border-color: rgba(59,130,246,0.45);
    box-shadow: 0 12px 35px rgba(0,0,0,0.30);
}}

.provider * {{
    color: #f8fafc !important;
}}

/* =========================
   ARCHITECTURE
========================= */

.arch {{
    padding: 28px;
    border-radius: 20px;
    background: #020617;
    border: 1px solid #1e3a5f;
    box-shadow: inset 0 0 40px rgba(37,99,235,0.05);
    overflow-x: auto;
}}

.arch pre {{
    color: #60a5fa !important;
    font-size: 15px;
    line-height: 1.8;
}}

/* =========================
   DIVIDER
========================= */

hr {{
    border-color: #172033 !important;
}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:26px;
            font-weight:900;
            color:#ffffff;
            margin-bottom:4px;
        ">
        🤖 HealTrip AI
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(t("subtitle"))

    st.markdown(
        f"""
        <div class="status">
            <span class="status-dot"></span>
            {t("online")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    selected_language = st.radio(
        t("language"),
        ["English", "العربية"],
        index=1 if ARABIC else 0,
        key="language_control",
    )

    new_language = (
        "Arabic"
        if selected_language == "العربية"
        else "English"
    )

    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

    st.divider()

    st.markdown(
        f"### {t('navigation')}"
    )

    nav = [
        ("assistant", t("assistant")),
        ("care", t("care")),
        ("providers", t("providers")),
        ("summary", t("summary")),
        ("architecture", t("architecture")),
    ]

    current_index = next(
        (
            i
            for i, (key, _) in enumerate(nav)
            if key == st.session_state.page
        ),
        0,
    )

    selected_nav = st.radio(
        "",
        [label for _, label in nav],
        index=current_index,
        key="nav_control",
    )

    for key, label in nav:
        if selected_nav == label:
            st.session_state.page = key

    st.divider()

    if st.button(
        t("new"),
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.conversation = []
        st.session_state.last_result = None
        st.rerun()

    st.divider()

    st.caption(
        "Prototype Database\n\n"
        "No Live Appointments\n\n"
        "Not a Diagnostic System"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
<div class="hero">

<div class="badge">
✦ {t("badge")}
</div>

<div class="hero-title">
{t("title")}
</div>

<div class="hero-subtitle">
{t("subtitle")}
</div>

<div class="hero-description">
{t("hero")}
</div>

<br>

<div class="status">
<span class="status-dot"></span>
{t("online")}
</div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# ASSISTANT
# ============================================================

if st.session_state.page == "assistant":

    st.markdown(
        f"""
        <div class="safety">
        <strong>⚠️ {t("safety")}</strong>
        <br><br>
        {t("safety_text")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns(
        [1.7, 1],
        gap="large",
    )

    with left:

        st.markdown(
            f"## {t('assistant_title')}"
        )

        st.caption(
            t("assistant_intro")
        )

        if not st.session_state.messages:

            q1, q2, q3 = st.columns(3)

            with q1:
                if st.button(
                    t("chest"),
                    use_container_width=True,
                ):
                    st.session_state.quick_prompt = (
                        "I have chest pain and I am not sure "
                        "what my next healthcare step should be."
                    )
                    st.rerun()

            with q2:
                if st.button(
                    t("cardiologist"),
                    use_container_width=True,
                ):
                    st.session_state.quick_prompt = (
                        "I want a cardiologist in Riyadh."
                    )
                    st.rerun()

            with q3:
                if st.button(
                    t("hospital"),
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
            t("placeholder")
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
                    t("thinking")
                ):

                    result = run_agent(
                        user_message=prompt,
                        conversation=st.session_state.conversation,
                    )

                answer = result["answer"]

                st.markdown(answer)

                if result.get("tools_used"):

                    with st.expander(
                        t("tools")
                    ):

                        for tool in result["tools_used"]:
                            st.success(
                                f"{tool}"
                            )

                if result.get("mode") in [
                    "fallback",
                    "local_fallback",
                ]:

                    with st.expander(
                        t("diagnostics")
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
            f"""
            <div class="ai-core">

                <div class="ai-orb">
                    🤖
                </div>

                <div class="ai-title">
                    {t("intelligence")}
                </div>

                <div class="ai-subtitle">
                    {t("intelligence_sub")}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="glass">
                <div class="card-title">
                    🧠 {t("reasoning")}
                </div>
                <div class="card-text">
                    {t("reasoning_text")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            f"""
            <div class="glass">
                <div class="card-title">
                    🛡️ {t("guardrails")}
                </div>
                <div class="card-text">
                    {t("guardrails_text")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            f"""
            <div class="glass">
                <div class="card-title">
                    🔒 {t("grounded")}
                </div>
                <div class="card-text">
                    {t("grounded_text")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CARE PATH
# ============================================================

elif st.session_state.page == "care":

    st.markdown(
        f"# 🧭 {t('care_title')}"
    )

    st.caption(
        t("care_intro")
    )

    steps = [
        ("01", "🧠", t("understand"), t("understand_text")),
        ("02", "🛡️", t("check"), t("check_text")),
        ("03", "💬", t("clarify"), t("clarify_text")),
        ("04", "🔎", t("tool"), t("tool_text")),
        ("05", "🔒", t("ground"), t("ground_text")),
        ("06", "✦", t("respond"), t("respond_text")),
    ]

    for number, icon, title, description in steps:

        col1, col2 = st.columns(
            [0.15, 0.85]
        )

        with col1:
            st.markdown(
                f"""
                <div style="
                    font-size:28px;
                    font-weight:900;
                    color:#60a5fa;
                ">
                {number}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"### {icon} {title}"
            )

            st.caption(
                description
            )

        st.divider()


# ============================================================
# PROVIDERS
# ============================================================

elif st.session_state.page == "providers":

    st.markdown(
        f"# 👨‍⚕️ {t('providers_title')}"
    )

    st.warning(
        t("demo")
    )

    tab1, tab2 = st.tabs(
        [
            f"👨‍⚕️ {t('doctors')}",
            f"🏥 {t('hospitals')}",
        ]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            specialty_options = [
                t("any"),
                "Cardiology",
                "Internal Medicine",
                "Pulmonology",
            ]

            selected_specialty = st.selectbox(
                t("specialty"),
                specialty_options,
                key="doctor_specialty",
            )

        with col2:

            city_options = [
                t("any"),
                "Riyadh",
                "Jeddah",
            ]

            selected_city = st.selectbox(
                t("city"),
                city_options,
                key="doctor_city",
            )

        specialty = (
            None
            if selected_specialty == t("any")
            else selected_specialty
        )

        city = (
            None
            if selected_city == t("any")
            else selected_city
        )

        doctors = search_doctors(
            specialty=specialty,
            city=city,
        )

        st.caption(
            f"{len(doctors)} {t('records')}"
        )

        for doctor in doctors:

            st.markdown(
                f"""
                <div class="provider">

                <h3>👨‍⚕️ {doctor["name"]}</h3>

                <p>
                <strong>{t("specialty")}:</strong>
                {doctor["specialty"]}
                </p>

                <p>
                <strong>{t("hospital")}:</strong>
                {doctor["hospital"]}
                </p>

                <p>
                <strong>{t("location")}:</strong>
                {doctor["city"]}, {doctor["country"]}
                </p>

                <p>
                <strong>{t("languages")}:</strong>
                {doctor["languages"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            hospital_city_display = st.selectbox(
                t("city"),
                [
                    t("any"),
                    "Riyadh",
                    "Jeddah",
                ],
                key="hospital_city",
            )

        with col2:

            emergency_only = st.checkbox(
                t("emergency"),
                key="emergency_filter",
            )

        hospital_city = (
            None
            if hospital_city_display == t("any")
            else hospital_city_display
        )

        hospitals = search_hospitals(
            city=hospital_city,
            emergency_only=emergency_only,
        )

        st.caption(
            f"{len(hospitals)} {t('records')}"
        )

        for hospital in hospitals:

            emergency_status = (
                t("available")
                if hospital["emergency_available"]
                else t("not_listed")
            )

            st.markdown(
                f"""
                <div class="provider">

                <h3>🏥 {hospital["name"]}</h3>

                <p>
                <strong>{t("location")}:</strong>
                {hospital["city"]}, {hospital["country"]}
                </p>

                <p>
                <strong>Specialties:</strong>
                {hospital["specialties"]}
                </p>

                <p>
                <strong>{t("emergency")}:</strong>
                {emergency_status}
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# PATIENT SUMMARY
# ============================================================

elif st.session_state.page == "summary":

    st.markdown(
        f"# 📋 {t('summary_title')}"
    )

    if not st.session_state.messages:

        st.info(
            t("start")
        )

    else:

        user_messages = [
            m["content"]
            for m in st.session_state.messages
            if m["role"] == "user"
        ]

        assistant_messages = [
            m["content"]
            for m in st.session_state.messages
            if m["role"] == "assistant"
        ]

        if user_messages:

            st.markdown(
                f"### {t('concern')}"
            )

            st.info(
                user_messages[-1]
            )

        if assistant_messages:

            st.markdown(
                f"### {t('guidance')}"
            )

            st.markdown(
                assistant_messages[-1]
            )

        st.divider()

        st.info(
            t("not_record")
        )


# ============================================================
# ARCHITECTURE
# ============================================================

elif st.session_state.page == "architecture":

    st.markdown(
        f"# 🏗️ {t('architecture_title')}"
    )

    architecture = """
Patient
   │
   ▼
Streamlit UI
   │
   ▼
Safety Layer
   │
   ▼
AI Agent
   │
   ├───────────────┐
   ▼               ▼
Doctor Tool   Hospital Tool
   │               │
   └───────┬───────┘
           ▼
     SQLite Database
           │
           ▼
    Grounded Results
           │
           ▼
      AI Response
"""

    st.markdown(
        f"""
        <div class="arch">
        <pre>{architecture}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        f"### {t('principles')}"
    )

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

    if ARABIC:
        principles = [
            "توجيه يركز على السلامة",
            "البحث عن مقدمي الخدمة باستخدام الأدوات",
            "الاعتماد على قاعدة البيانات",
            "عدم اختلاق الأطباء",
            "عدم اختلاق المواعيد أو التوفر",
            "تفاعل متعدد اللغات",
            "ذاكرة محادثة داخل الجلسة",
            "استجابة احتياطية عند تعذر الذكاء الاصطناعي",
            "حدود واضحة للنموذج التجريبي",
        ]

    for item in principles:
        st.write(f"✓ {item}")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    t("footer")
)
