import streamlit as st
import requests
import sys
from exception.exceptions import TradingBotException

BASE_URL = "http://localhost:8000"

# Setup
st.set_page_config(
    page_title="📈 Stock Market Agentic AI Chatbot",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for a sleek look
st.markdown("""
    <style>
    body {
        background-color: #f4f6f8;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #f4f6f8;
    }
    .chat-bubble {
        padding: 1rem;
        margin: 10px 0;
        border-radius: 15px;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .chat-bubble:hover {
        transform: scale(1.01);
    }
    .user {
        background-color: #d6e4ff;
        color: #003366;
        margin-left: auto;
    }
    .bot {
        background-color: #d2f0db;
        color: #1a3c1d;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }
    .agent-badge {
        background-color: #e0e0e0;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 12px;
        margin-top: 4px;
        display: inline-block;
    }
    .stTextInput>div>div>input {
        padding: 10px;
        font-size: 16px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 16px;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #005ce6, #00a8e6);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Stock Market Agentic AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: Upload docs
with st.sidebar:
    st.header("📄 Upload Market Reports")
    st.caption("Upload PDF or DOCX files (research, earnings, etc.)")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("📤 Upload and Ingest"):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                file_data = f.read()
                if not file_data:
                    continue
                files.append(("files", (f.name, file_data, f.type)))

            if files:
                try:
                    with st.spinner("Uploading..."):
                        response = requests.post(f"{BASE_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success("✅ Uploaded successfully!")
                        else:
                            st.error("❌ Upload failed: " + response.text)
                except Exception as e:
                    raise TradingBotException(e, sys)
        else:
            st.warning("⚠️ No valid files selected.")

# Agent selector
st.subheader("🤖 Choose Your Assistant")
agent_role = st.selectbox(
    "Select Agent",
    ["AI Trader 🧑‍💼", "AI Analyst 📊", "AI Risk Manager ⚠️"],
    index=1
)

# Chat display
chat_placeholder = st.empty()
with chat_placeholder.container():
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        agent = msg.get("agent", "")
        bubble_class = "user" if role == "user" else "bot"
        name = "🧑 You" if role == "user" else f"{agent}"

        st.markdown(
            f"""
            <div class='chat-container'>
                <div class='chat-bubble {bubble_class}'>
                    <strong>{name}</strong><br>{content}
                    {"<div class='agent-badge'>" + agent + "</div>" if role == "bot" else ""}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

# Chat input
st.markdown("---")
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Ask your question", placeholder="E.g., What’s your analysis on Reliance?")
    submit_button = st.form_submit_button("🚀 Send")

# On submit
if submit_button and user_input.strip():
    try:
        agent_id = agent_role.split()[0]  # AI, Analyst, Risk
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "agent": agent_role
        })

        with st.spinner("Agent thinking..."):
            payload = {"question": user_input, "agent": agent_id}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.messages.append({
                "role": "bot",
                "content": answer,
                "agent": agent_role
            })
            st.rerun()
        else:
            st.error("❌ Bot failed: " + response.text)

    except Exception as e:
        raise TradingBotException(e, sys)
