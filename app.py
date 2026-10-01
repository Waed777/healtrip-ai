import streamlit as st

st.set_page_config(
    page_title="HealTrip AI",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 HealTrip AI")
st.caption("Patient Decision Assistant")

st.markdown("""
### Welcome to HealTrip AI

Describe your health concern and the assistant will help you determine
the appropriate next step.

> HealTrip AI provides decision support only. It does not diagnose medical conditions.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Describe your concern..."
)

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    response = (
        "Thank you for sharing your concern. "
        "The AI decision engine will analyze your symptoms, "
        "ask clarifying questions when needed, and determine "
        "whether you may need urgent medical evaluation, "
        "a specialist consultation, or further medical advice."
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)
