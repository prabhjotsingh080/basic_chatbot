import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Chat Assistant", layout="wide", initial_sidebar_state="collapsed")

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set GEMINI_API_KEY in .env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    USE_SUPABASE = True
else:
    USE_SUPABASE = False
    st.warning("⚠️ Supabase not configured. Running in memory-only mode.")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = []

# Supabase Functions
def create_new_session():
    """Create a new chat session in Supabase"""
    if not USE_SUPABASE:
        return None
    
    try:
        response = supabase.table('chat_sessions').insert({
            'title': 'New Chat',
            'user_id': None  # For now, no authentication
        }).execute()
        
        if response.data:
            return response.data[0]['id']
    except Exception as e:
        st.error(f"Error creating session: {str(e)}")
    return None

def save_message(session_id, role, content):
    """Save a message to Supabase"""
    if not USE_SUPABASE or not session_id:
        return
    
    try:
        supabase.table('messages').insert({
            'session_id': session_id,
            'role': role,
            'content': content
        }).execute()
    except Exception as e:
        st.error(f"Error saving message: {str(e)}")

def load_messages(session_id):
    """Load messages from a specific session"""
    if not USE_SUPABASE or not session_id:
        return []
    
    try:
        response = supabase.table('messages')\
            .select('*')\
            .eq('session_id', session_id)\
            .order('created_at')\
            .execute()
        
        if response.data:
            return [{'role': msg['role'], 'content': msg['content']} for msg in response.data]
    except Exception as e:
        st.error(f"Error loading messages: {str(e)}")
    return []

def load_all_sessions():
    """Load all chat sessions"""
    if not USE_SUPABASE:
        return []
    
    try:
        response = supabase.table('chat_sessions')\
            .select('*')\
            .order('updated_at', desc=True)\
            .limit(20)\
            .execute()
        
        if response.data:
            return response.data
    except Exception as e:
        st.error(f"Error loading sessions: {str(e)}")
    return []

def update_session_title(session_id, title):
    """Update session title based on first message"""
    if not USE_SUPABASE or not session_id:
        return
    
    try:
        supabase.table('chat_sessions')\
            .update({'title': title[:50]})\
            .eq('id', session_id)\
            .execute()
    except Exception as e:
        st.error(f"Error updating title: {str(e)}")

def delete_session(session_id):
    """Delete a chat session"""
    if not USE_SUPABASE or not session_id:
        return
    
    try:
        supabase.table('chat_sessions').delete().eq('id', session_id).execute()
    except Exception as e:
        st.error(f"Error deleting session: {str(e)}")

# Theme colors
def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            'bg': '#1a1a2e',
            'secondary_bg': '#16213e',
            'text': '#ffffff',
            'input_bg': '#0f3460',
            'accent': '#4a90e2',
            'user_msg': '#2c3e50',
            'ai_msg': '#34495e',
            'sidebar_bg': '#16213e'
        }
    else:
        return {
            'bg': '#f5f7fa',
            'secondary_bg': '#ffffff',
            'text': '#2c3e50',
            'input_bg': '#e8f4f8',
            'accent': '#4a90e2',
            'user_msg': '#e3f2fd',
            'ai_msg': '#f0f4f8',
            'sidebar_bg': '#ffffff'
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
    [data-testid="stSidebar"] {{
        background-color: {colors['sidebar_bg']};
    }}
    .session-item {{
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        cursor: pointer;
        background-color: {colors['input_bg']};
        color: {colors['text']};
    }}
    .session-item:hover {{
        opacity: 0.8;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar - Chat History
with st.sidebar:
    st.markdown("### 💬 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.current_session_id = None
        st.rerun()
    
    st.markdown("---")
    
    if USE_SUPABASE:
        # Load sessions
        sessions = load_all_sessions()
        
        for session in sessions:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    session['title'][:30], 
                    key=f"session_{session['id']}",
                    use_container_width=True
                ):
                    # Load this session
                    st.session_state.current_session_id = session['id']
                    st.session_state.messages = load_messages(session['id'])
                    st.session_state.chat_session = model.start_chat(history=[])
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{session['id']}"):
                    delete_session(session['id'])
                    if st.session_state.current_session_id == session['id']:
                        st.session_state.messages = []
                        st.session_state.current_session_id = None
                    st.rerun()

# Header with buttons
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
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

def handle_submit():
    if st.session_state.temp_input.strip():
        user_msg = st.session_state.temp_input
        
        # Create new session if needed
        if USE_SUPABASE and not st.session_state.current_session_id:
            st.session_state.current_session_id = create_new_session()
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Save to Supabase
        if USE_SUPABASE and st.session_state.current_session_id:
            save_message(st.session_state.current_session_id, "user", user_msg)
            
            # Update session title with first message
            if len(st.session_state.messages) == 1:
                update_session_title(st.session_state.current_session_id, user_msg)
        
        # Get AI response
        try:
            response = st.session_state.chat_session.send_message(user_msg)
            ai_response = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Save AI response to Supabase
            if USE_SUPABASE and st.session_state.current_session_id:
                save_message(st.session_state.current_session_id, "assistant", ai_response)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.session_state.temp_input = ""

user_input = st.text_input(
    "Type your message...", 
    key="temp_input", 
    on_change=handle_submit, 
    label_visibility="collapsed"
)