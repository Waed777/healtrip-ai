import streamlit as st

from database import (
    initialize_database,
    search_doctors,
    search_hospitals,
)

from agent import run_agent


# ============================================================
# PAGE CONFIG
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

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "page" not in st.session_state:
    st.session_state.page = "assistant"


# ============================================================
# LANGUAGE
# ============================================================

LANG = st.session_state.language

ARABIC = LANG == "Arabic"


# ============================================================
# TRANSLATIONS
# ============================================================

T = {
    "English": {
        "app_name": "HealTrip AI",
        "tagline": "Patient Decision Assistant",
        "language": "Language",
        "navigation": "Navigation",
        "assistant": "🤖 AI Assistant",
        "care_path": "🧭 Care Path",
        "providers": "👨‍⚕️ Providers",
        "summary": "📋 Patient Summary",
        "architecture": "🏗️ Architecture",
        "new": "🆕 New Assessment",
        "prototype": "Prototype database",
        "no_live": "No live appointments",
        "not_diagnostic": "Not a diagnostic system",
        "badge": "AI HEALTHCARE NAVIGATION",
        "hero_text": (
            "A safety-aware AI assistant designed to help users "
            "navigate their next healthcare step using structured "
            "reasoning, database tools, and multilingual interaction."
        ),
        "safety_title": "⚠️ Safety Notice",
        "safety_text": (
            "HealTrip AI is a technical prototype. "
            "It does not diagnose medical conditions and does not "
            "replace professional medical care."
        ),
        "assistant_title": "AI Patient Assistant",
        "assistant_info": (
            "Tell HealTrip AI what you need. You can describe symptoms, "
            "ask for a specialist, or search for a hospital."
        ),
        "quick_chest": "🫀 Chest pain",
        "quick_doctor": "👨‍⚕️ Cardiologist",
        "quick_hospital": "🏥 Hospital",
        "chat_placeholder": "Describe your situation...",
        "thinking": "HealTrip AI is thinking...",
        "tool_trace": "🔧 Agent Tool Trace",
        "executed": "Executed",
        "diagnostics": "Developer diagnostics",
        "intelligence": "HealTrip Intelligence",
        "reason": "Reason → Check Safety → Use Tools → Respond",
        "ai_reasoning": "🧠 AI Reasoning",
        "ai_reasoning_text": (
            "The assistant interprets the user's request and determines "
            "whether additional information or a database tool is required."
        ),
        "safety_layer": "🛡️ Safety Layer",
        "safety_layer_text": (
            "Potential urgent symptoms are checked before normal "
            "provider recommendations."
        ),
        "grounded": "🔒 Grounded Results",
        "grounded_text": (
            "Provider information comes from the prototype database "
            "rather than being invented by the model."
        ),
        "care_title": "🧭 Care Path",
        "care_intro": (
            "A transparent view of how HealTrip AI approaches a request."
        ),
        "understand": "Understand",
        "understand_text": "Interpret the user's concern and context.",
        "check": "Safety Check",
        "check_text": "Identify signals that may require urgent evaluation.",
        "clarify": "Clarify",
        "clarify_text": "Ask for important missing information.",
        "choose": "Choose Tool",
        "choose_text": "Search the appropriate provider or hospital data.",
        "ground": "Ground",
        "ground_text": "Use returned database records only.",
        "respond": "Respond",
        "respond_text": "Provide a clear next-step explanation.",
        "provider_title": "👨‍⚕️ Provider Search",
        "demo_warning": (
            "Demo database only. These records are synthetic prototype "
            "data. They do not represent live availability or "
            "real-world verification."
        ),
        "doctors": "👨‍⚕️ Doctors",
        "hospitals": "🏥 Hospitals",
        "specialty": "Specialty",
        "city": "City",
        "any": "Any",
        "emergency_only": "Emergency capability only",
        "records": "provider records found",
        "hospital_records": "hospital records found",
        "emergency_available": "Available",
        "not_listed": "Not listed",
        "location": "Location",
        "languages": "Languages",
        "hospital": "Hospital",
        "specialties": "Specialties",
        "summary_title": "📋 Patient Summary",
        "start_conversation": "Start a conversation with HealTrip AI first.",
        "conversation_overview": "🧑‍⚕️ Conversation Overview",
        "patient_concern": "Patient concern",
        "latest_guidance": "Latest assistant guidance",
        "summary_warning": (
            "This summary is generated from the conversation "
            "and is not a medical record."
        ),
        "architecture_title": "🏗️ System Architecture",
        "engineering": "Engineering Principles",
        "footer": (
            "HealTrip AI • Safety-aware • Tool-using • "
            "Multilingual • Database-grounded • Prototype"
        ),
        "principles": [
            "Safety-first routing",
            "Tool-based provider discovery",
            "Database-grounded responses",
            "No invented providers",
            "No invented availability",
            "Multilingual interaction",
            "Session-based conversation memory",
            "Graceful AI fallback",
            "Clear prototype boundaries",
        ],
    },

    "Arabic": {
        "app_name": "HealTrip AI",
        "tagline": "مساعد اتخاذ القرار الصحي",
        "language": "اللغة",
        "navigation": "التنقل",
        "assistant": "🤖 المساعد الذكي",
        "care_path": "🧭 مسار الرعاية",
        "providers": "👨‍⚕️ الأطباء والمستشفيات",
        "summary": "📋 ملخص الحالة",
        "architecture": "🏗️ بنية النظام",
        "new": "🆕 تقييم جديد",
        "prototype": "قاعدة بيانات تجريبية",
        "no_live": "لا توجد مواعيد مباشرة",
        "not_diagnostic": "ليس نظامًا للتشخيص",
        "badge": "منصة ذكية للتنقل في الرعاية الصحية",
        "hero_text": (
            "مساعد ذكي وآمن يساعد المستخدم على فهم الخطوة الصحية "
            "التالية من خلال تحليل الطلب، واستخدام أدوات البحث، "
            "وقاعدة بيانات منظمة، مع دعم العربية والإنجليزية."
        ),
        "safety_title": "⚠️ تنبيه السلامة",
        "safety_text": (
            "HealTrip AI نموذج تقني تجريبي. لا يقوم بتشخيص الحالات "
            "الطبية ولا يحل محل الطبيب أو خدمات الرعاية الصحية."
        ),
        "assistant_title": "المساعد الصحي الذكي",
        "assistant_info": (
            "أخبر HealTrip AI بما تحتاجه. يمكنك وصف الأعراض، "
            "طلب طبيب متخصص، أو البحث عن مستشفى."
        ),
        "quick_chest": "🫀 ألم في الصدر",
        "quick_doctor": "👨‍⚕️ طبيب قلب",
        "quick_hospital": "🏥 مستشفى",
        "chat_placeholder": "اكتب حالتك أو سؤالك هنا...",
        "thinking": "جاري تحليل طلبك...",
        "tool_trace": "🔧 سجل استخدام الأدوات",
        "executed": "تم تشغيل",
        "diagnostics": "تشخيص للمطور",
        "intelligence": "ذكاء HealTrip",
        "reason": "تحليل ← فحص السلامة ← استخدام الأدوات ← الرد",
        "ai_reasoning": "🧠 تحليل ذكي",
        "ai_reasoning_text": (
            "يفهم المساعد طلب المستخدم ويحدد ما إذا كان يحتاج "
            "إلى معلومات إضافية أو إلى البحث في قاعدة البيانات."
        ),
        "safety_layer": "🛡️ طبقة السلامة",
        "safety_layer_text": (
            "يتم فحص الأعراض التي قد تشير إلى حالة عاجلة "
            "قبل تقديم خيارات الرعاية."
        ),
        "grounded": "🔒 نتائج موثوقة بالبيانات",
        "grounded_text": (
            "معلومات الأطباء والمستشفيات تأتي من قاعدة البيانات "
            "التجريبية بدلًا من اختلاقها بواسطة النموذج."
        ),
        "care_title": "🧭 مسار الرعاية",
        "care_intro": (
            "طريقة واضحة وشفافة لكيفية تعامل HealTrip AI مع طلب المستخدم."
        ),
        "understand": "الفهم",
        "understand_text": "فهم المشكلة والسياق الذي يقدمه المستخدم.",
        "check": "فحص السلامة",
        "check_text": "تحديد المؤشرات التي قد تحتاج إلى تقييم عاجل.",
        "clarify": "الاستيضاح",
        "clarify_text": "طرح الأسئلة المهمة عند نقص المعلومات.",
        "choose": "اختيار الأداة",
        "choose_text": "البحث في بيانات الأطباء أو المستشفيات المناسبة.",
        "ground": "الاعتماد على البيانات",
        "ground_text": "استخدام السجلات التي أعادتها قاعدة البيانات فقط.",
        "respond": "الاستجابة",
        "respond_text": "تقديم شرح واضح للخطوة الصحية التالية.",
        "provider_title": "👨‍⚕️ البحث عن الأطباء والمستشفيات",
        "demo_warning": (
            "قاعدة بيانات تجريبية فقط. السجلات المعروضة بيانات "
            "افتراضية للبروتوتايب وليست مواعيد مباشرة أو تحققًا "
            "من بيانات مقدمي الخدمة في العالم الحقيقي."
        ),
        "doctors": "👨‍⚕️ الأطباء",
        "hospitals": "🏥 المستشفيات",
        "specialty": "التخصص",
        "city": "المدينة",
        "any": "الكل",
        "emergency_only": "طوارئ فقط",
        "records": "سجل طبيب متاح",
        "hospital_records": "سجل مستشفى متاح",
        "emergency_available": "متاحة",
        "not_listed": "غير مذكورة",
        "location": "الموقع",
        "languages": "اللغات",
        "hospital": "المستشفى",
        "specialties": "التخصصات",
        "summary_title": "📋 ملخص الحالة",
        "start_conversation": "ابدأ محادثة مع HealTrip AI أولًا.",
        "conversation_overview": "🧑‍⚕️ ملخص المحادثة",
        "patient_concern": "مشكلة المستخدم",
        "latest_guidance": "آخر توجيه من المساعد",
        "summary_warning": (
            "هذا الملخص مستخرج من المحادثة وليس سجلًا طبيًا."
        ),
        "architecture_title": "🏗️ بنية النظام",
        "engineering": "مبادئ هندسية",
        "footer": (
            "HealTrip AI • آمن • يعتمد على الأدوات • "
            "متعدد اللغات • يعتمد على البيانات • نموذج تجريبي"
        ),
        "principles": [
            "توجيه يركز على السلامة",
            "البحث عن مقدمي الخدمة باستخدام الأدوات",
            "الاعتماد على قاعدة البيانات",
            "عدم اختلاق الأطباء",
            "عدم اختلاق المواعيد أو التوفر",
            "تفاعل متعدد اللغات",
            "ذاكرة محادثة داخل الجلسة",
            "استجابة احتياطية عند تعذر الذكاء الاصطناعي",
            "حدود واضحة للنموذج التجريبي",
        ],
    },
}


def tr(key):
    return T[st.session_state.language][key]


# ============================================================
# RTL / DARK UI
# ============================================================

if ARABIC:
    direction = "rtl"
    text_align = "right"
else:
    direction = "ltr"
    text_align = "left"


st.markdown(
    f"""
<style>

html, body, [class*="css"] {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}}

.stApp {{
    background: #050b14 !important;
    color: #f8fafc !important;
}}

[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(37, 99, 235, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 80%,
            rgba(14, 116, 144, 0.10),
            transparent 30%
        ),
        #050b14 !important;
}}

[data-testid="stHeader"] {{
    background: rgba(5, 11, 20, 0.85) !important;
}}

[data-testid="stSidebar"] {{
    background: #08111f !important;
    border-right: 1px solid #1e293b;
}}

[data-testid="stSidebar"] * {{
    color: #f8fafc !important;
}}

.block-container {{
    max-width: 1250px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}}

h1, h2, h3, h4, h5, h6,
p, li, label, span, div {{
    color: #f8fafc;
}}

.stMarkdown,
.stText,
.stCaption {{
    color: #f8fafc !important;
}}

.stCaption {{
    color: #94a3b8 !important;
}}

[data-testid="stMarkdownContainer"] {{
    direction: {direction};
    text-align: {text_align};
}}

[data-testid="stChatMessage"] {{
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid #1e293b !important;
    border-radius: 18px !important;
    margin-bottom: 10px;
}}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div {{
    color: #f8fafc !important;
}}

[data-testid="stChatInput"] {{
    background: #0f172a !important;
}}

[data-testid="stChatInput"] textarea {{
    color: #ffffff !important;
    background: #0f172a !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: #94a3b8 !important;
}}

.stButton > button {{
    background: #111c2f !important;
    color: #f8fafc !important;
    border: 1px solid #263650 !important;
    border-radius: 12px !important;
    min-height: 42px;
}}

.stButton > button:hover {{
    border-color: #3b82f6 !important;
    color: #ffffff !important;
    background: #16243b !important;
}}

.stSelectbox > div > div,
.stMultiSelect > div > div {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #334155 !important;
}}

.stSelectbox label,
.stCheckbox label,
.stRadio label {{
    color: #e2e8f0 !important;
}}

[data-baseweb="select"] {{
    background: #0f172a !important;
}}

[data-baseweb="select"] * {{
    color: #ffffff !important;
}}

[data-baseweb="popover"] {{
    background: #0f172a !important;
}}

[role="option"] {{
    background: #0f172a !important;
    color: #ffffff !important;
}}

[role="option"]:hover {{
    background: #1e3a5f !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    color: #cbd5e1 !important;
    background: #0f172a !important;
    border-radius: 10px !important;
}}

.stTabs [aria-selected="true"] {{
    color: #ffffff !important;
    background: #1d4ed8 !important;
}}

[data-testid="stExpander"] {{
    background: #0b1424 !important;
    border: 1px solid #24344d !important;
    border-radius: 14px !important;
}}

[data-testid="stExpander"] * {{
    color: #f8fafc !important;
}}

[data-testid="stAlert"] {{
    background: #0d1829 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
}}

.hero {{
    padding: 38px;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            #0b1424 0%,
            #101c34 55%,
            #123b73 100%
        );
    border: 1px solid #243b5c;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    margin-bottom: 25px;
    direction: {direction};
    text-align: {text_align};
}}

.hero-badge {{
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: #102a4d;
    border: 1px solid #24538b;
    color: #93c5fd !important;
    font-size: 13px;
    margin-bottom: 14px;
}}

.hero-title {{
    font-size: 48px;
    line-height: 1.1;
    font-weight: 800;
    color: #ffffff !important;
}}

.hero-subtitle {{
    color: #bfdbfe !important;
    font-size: 20px;
    margin-top: 8px;
}}

.hero-description {{
    color: #cbd5e1 !important;
    max-width: 850px;
    font-size: 16px;
    line-height: 1.8;
}}

.card {{
    padding: 22px;
    border-radius: 20px;
    background: #0c1728;
    border: 1px solid #23334d;
    margin-bottom: 15px;
}}

.card-title {{
    color: #ffffff !important;
    font-size: 18px;
    font-weight: 700;
}}

.card-text {{
    color: #aebdd1 !important;
    font-size: 14px;
    line-height: 1.7;
}}

.robot {{
    text-align: center;
    font-size: 82px;
    padding: 10px;
}}

.robot-title {{
    text-align: center;
    color: #ffffff !important;
    font-size: 23px;
    font-weight: 800;
}}

.robot-text {{
    text-align: center;
    color: #94a3b8 !important;
}}

.safety-box {{
    padding: 20px;
    border-radius: 18px;
    background: #201a0c;
    border: 1px solid #6b4f16;
    color: #f8fafc !important;
    direction: {direction};
    text-align: {text_align};
}}

.section-title {{
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 15px;
}}

.provider-card {{
    padding: 20px;
    border-radius: 18px;
    background: #0c1728;
    border: 1px solid #23334d;
    margin-bottom: 15px;
}}

.provider-card * {{
    color: #f8fafc !important;
}}

.arch {{
    padding: 24px;
    border-radius: 18px;
    background: #08111f;
    border: 1px solid #24466f;
    overflow-x: auto;
}}

.arch pre {{
    color: #93c5fd !important;
    font-size: 15px;
    line-height: 1.7;
}}

hr {{
    border-color: #1e293b !important;
}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(f"# 🤖 {tr('app_name')}")
    st.caption(tr("tagline"))

    st.divider()

    language_display = st.radio(
        tr("language"),
        ["English", "العربية"],
        index=0 if not ARABIC else 1,
        key="language_selector",
    )

    new_language = (
        "Arabic"
        if language_display == "العربية"
        else "English"
    )

    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

    st.divider()

    st.markdown(f"### {tr('navigation')}")

    nav_options = [
        tr("assistant"),
        tr("care_path"),
        tr("providers"),
        tr("summary"),
        tr("architecture"),
    ]

    current_index = 0

    if st.session_state.page == "care":
        current_index = 1
    elif st.session_state.page == "providers":
        current_index = 2
    elif st.session_state.page == "summary":
        current_index = 3
    elif st.session_state.page == "architecture":
        current_index = 4

    selected_page = st.radio(
        "",
        nav_options,
        index=current_index,
        key="navigation_selector",
    )

    if selected_page == tr("assistant"):
        st.session_state.page = "assistant"
    elif selected_page == tr("care_path"):
        st.session_state.page = "care"
    elif selected_page == tr("providers"):
        st.session_state.page = "providers"
    elif selected_page == tr("summary"):
        st.session_state.page = "summary"
    elif selected_page == tr("architecture"):
        st.session_state.page = "architecture"

    st.divider()

    if st.button(
        tr("new"),
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.conversation = []
        st.session_state.last_result = None
        st.rerun()

    st.divider()

    st.caption(
        f"{tr('prototype')}\n\n"
        f"{tr('no_live')}\n\n"
        f"{tr('not_diagnostic')}"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
<div class="hero">

<div class="hero-badge">
{tr("badge")}
</div>

<div class="hero-title">
🤖 HealTrip AI
</div>

<div class="hero-subtitle">
{tr("tagline")}
</div>

<div class="hero-description">
{tr("hero_text")}
</div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AI ASSISTANT
# ============================================================

if st.session_state.page == "assistant":

    st.markdown(
        f"""
<div class="safety-box">

<strong>{tr("safety_title")}</strong>

<br><br>

{tr("safety_text")}

<br><br>

If symptoms may require urgent evaluation,
seek appropriate medical attention.

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns([1.7, 1])

    with left:

        st.markdown(
            f'<div class="section-title">{tr("assistant_title")}</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.messages:

            st.info(tr("assistant_info"))

            q1, q2, q3 = st.columns(3)

            with q1:
                if st.button(
                    tr("quick_chest"),
                    use_container_width=True,
                ):
                    st.session_state.quick_prompt = (
                        "I have chest pain and I am not sure "
                        "what my next healthcare step should be."
                    )
                    st.rerun()

            with q2:
                if st.button(
                    tr("quick_doctor"),
                    use_container_width=True,
                ):
                    st.session_state.quick_prompt = (
                        "I want a cardiologist in Riyadh."
                    )
                    st.rerun()

            with q3:
                if st.button(
                    tr("quick_hospital"),
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
                st.markdown(message["content"])

        prompt = st.chat_input(
            tr("chat_placeholder")
        )

        if "quick_prompt" in st.session_state:
            prompt = st.session_state.pop("quick_prompt")

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

                with st.spinner(tr("thinking")):

                    result = run_agent(
                        user_message=prompt,
                        conversation=st.session_state.conversation,
                    )

                answer = result["answer"]

                st.markdown(answer)

                if result.get("tools_used"):

                    with st.expander(
                        tr("tool_trace")
                    ):

                        for tool in result["tools_used"]:
                            st.success(
                                f"{tr('executed')}: {tool}"
                            )

                if result.get("mode") in ["fallback", "local_fallback"]:

                    with st.expander(
                        tr("diagnostics")
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
<div class="robot">
🤖
</div>

<div class="robot-title">
{tr("intelligence")}
</div>

<div class="robot-text">
{tr("reason")}
</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            f"""
<div class="card">

<div class="card-title">
{tr("ai_reasoning")}
</div>

<div class="card-text">
{tr("ai_reasoning_text")}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div class="card">

<div class="card-title">
{tr("safety_layer")}
</div>

<div class="card-text">
{tr("safety_layer_text")}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div class="card">

<div class="card-title">
{tr("grounded")}
</div>

<div class="card-text">
{tr("grounded_text")}
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
        f'<div class="section-title">{tr("care_title")}</div>',
        unsafe_allow_html=True,
    )

    st.write(tr("care_intro"))

    steps = [
        ("01", tr("understand"), tr("understand_text")),
        ("02", tr("check"), tr("check_text")),
        ("03", tr("clarify"), tr("clarify_text")),
        ("04", tr("choose"), tr("choose_text")),
        ("05", tr("ground"), tr("ground_text")),
        ("06", tr("respond"), tr("respond_text")),
    ]

    for number, title, description in steps:

        c1, c2 = st.columns([0.15, 0.85])

        with c1:
            st.markdown(f"### {number}")

        with c2:
            st.markdown(f"### {title}")
            st.write(description)

        st.divider()


# ============================================================
# PROVIDERS
# ============================================================

elif st.session_state.page == "providers":

    st.markdown(
        f'<div class="section-title">{tr("provider_title")}</div>',
        unsafe_allow_html=True,
    )

    st.warning(tr("demo_warning"))

    tab1, tab2 = st.tabs(
        [
            tr("doctors"),
            tr("hospitals"),
        ]
    )

    # --------------------------------------------------------
    # DOCTORS
    # --------------------------------------------------------

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            specialty_options = [
                tr("any"),
                "Cardiology",
                "Internal Medicine",
                "Pulmonology",
            ]

            specialty_display = st.selectbox(
                tr("specialty"),
                specialty_options,
                key="doctor_specialty",
            )

        with col2:

            city_options = [
                tr("any"),
                "Riyadh",
                "Jeddah",
            ]

            city_display = st.selectbox(
                tr("city"),
                city_options,
                key="doctor_city",
            )

        specialty_value = (
            None
            if specialty_display == tr("any")
            else specialty_display
        )

        city_value = (
            None
            if city_display == tr("any")
            else city_display
        )

        doctors = search_doctors(
            specialty=specialty_value,
            city=city_value,
        )

        st.write(
            f"**{len(doctors)} {tr('records')}**"
        )

        for doctor in doctors:

            st.markdown(
                f"""
<div class="provider-card">

<h3>👨‍⚕️ {doctor["name"]}</h3>

<p><strong>{tr("specialty")}:</strong>
{doctor["specialty"]}</p>

<p><strong>{tr("hospital")}:</strong>
{doctor["hospital"]}</p>

<p><strong>{tr("location")}:</strong>
{doctor["city"]}, {doctor["country"]}</p>

<p><strong>{tr("languages")}:</strong>
{doctor["languages"]}</p>

</div>
""",
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # HOSPITALS
    # --------------------------------------------------------

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            hospital_city_display = st.selectbox(
                tr("city"),
                [
                    tr("any"),
                    "Riyadh",
                    "Jeddah",
                ],
                key="hospital_city",
            )

        with col2:

            emergency_only = st.checkbox(
                tr("emergency_only"),
                key="emergency_only",
            )

        hospital_city = (
            None
            if hospital_city_display == tr("any")
            else hospital_city_display
        )

        hospitals = search_hospitals(
            city=hospital_city,
            emergency_only=emergency_only,
        )

        st.write(
            f"**{len(hospitals)} {tr('hospital_records')}**"
        )

        for hospital in hospitals:

            emergency_status = (
                tr("emergency_available")
                if hospital["emergency_available"]
                else tr("not_listed")
            )

            st.markdown(
                f"""
<div class="provider-card">

<h3>🏥 {hospital["name"]}</h3>

<p><strong>{tr("location")}:</strong>
{hospital["city"]}, {hospital["country"]}</p>

<p><strong>{tr("specialties")}:</strong>
{hospital["specialties"]}</p>

<p><strong>{tr("emergency_only")}:</strong>
{emergency_status}</p>

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# PATIENT SUMMARY
# ============================================================

elif st.session_state.page == "summary":

    st.markdown(
        f'<div class="section-title">{tr("summary_title")}</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:

        st.info(tr("start_conversation"))

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
            f"### {tr('conversation_overview')}"
        )

        if user_messages:

            st.markdown(
                f"**{tr('patient_concern')}**"
            )

            st.info(user_messages[-1])

        if assistant_messages:

            st.markdown(
                f"**{tr('latest_guidance')}**"
            )

            st.markdown(assistant_messages[-1])

        st.divider()

        st.markdown("### 🛡️ Safety")

        st.info(tr("summary_warning"))


# ============================================================
# ARCHITECTURE
# ============================================================

elif st.session_state.page == "architecture":

    st.markdown(
        f'<div class="section-title">{tr("architecture_title")}</div>',
        unsafe_allow_html=True,
    )

    architecture_text = """
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
"""

    st.markdown(
        f"""
<div class="arch">

<pre>{architecture_text}</pre>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        f"### {tr('engineering')}"
    )

    for item in T[st.session_state.language]["principles"]:
        st.write(f"✓ {item}")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(tr("footer"))
