import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(page_title="Chat Assistant", layout="wide", initial_sidebar_state="collapsed")

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("Please set GEMINI_API_KEY environment variable")
    st.stop()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            'bg': '#1a1a2e',
            'secondary_bg': '#16213e',
            'text': '#ffffff',
            'input_bg': '#0f3460',
            'accent': '#4a90e2',
            'user_msg': '#2c3e50',
            'ai_msg': '#34495e'
        }
    else:
        return {
            'bg': '#f5f7fa',
            'secondary_bg': '#ffffff',
            'text': '#2c3e50',
            'input_bg': '#e8f4f8',
            'accent': '#4a90e2',
            'user_msg': '#e3f2fd',
            'ai_msg': '#f0f4f8'
        }

colors = get_theme_colors()

# Custom CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: {colors['bg']};
    }}
    .main .block-container {{
        padding-top: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }}
    .chat-message {{
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }}
    .user-message {{
        background-color: {colors['user_msg']};
        margin-left: 2rem;
    }}
    .ai-message {{
        background-color: {colors['ai_msg']};
        margin-right: 2rem;
    }}
    .message-label {{
        font-weight: 600;
        font-size: 0.85rem;
        color: {colors['accent']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .message-text {{
        color: {colors['text']};
        line-height: 1.6;
    }}
    .welcome-text {{
        text-align: center;
        padding: 3rem 2rem;
        color: {colors['text']};
    }}
    .welcome-title {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {colors['accent']}, #64b5f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    .welcome-subtitle {{
        font-size: 1.2rem;
        color: {colors['text']};
        opacity: 0.7;
    }}
    div[data-testid="stTextInput"] > div > div {{
        background-color: {colors['input_bg']};
    }}
    div[data-testid="stTextInput"] input {{
        color: {colors['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Header with buttons
col1, col2 = st.columns([6, 1])
with col2:
    btn_cols = st.columns(2)
    with btn_cols[0]:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with btn_cols[1]:
        if st.button("➕", key="new_chat"):
            st.session_state.messages = []
            st.session_state.chat_session = model.start_chat(history=[])
            st.rerun()

# Chat display area
if not st.session_state.messages:
    st.markdown(f"""
    <div class="welcome-text">
        <div class="welcome-title">Hello!</div>
        <div class="welcome-subtitle">How can I assist you today?</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        msg_class = "user-message" if msg["role"] == "user" else "ai-message"
        label = "You" if msg["role"] == "user" else "Assistant"
        st.markdown(f"""
        <div class="chat-message {msg_class}">
            <div class="message-label">{label}</div>
            <div class="message-text">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Input area
st.markdown("<br>", unsafe_allow_html=True)

# Use a callback to handle submission
def handle_submit():
    if st.session_state.temp_input.strip():
        user_msg = st.session_state.temp_input
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        try:
            response = st.session_state.chat_session.send_message(user_msg)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.session_state.temp_input = ""

user_input = st.text_input("Type your message...", key="temp_input", on_change=handle_submit, label_visibility="collapsed")