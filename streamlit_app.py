import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Chat Assistant", layout="wide", initial_sidebar_state="expanded")

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set GEMINI_API_KEY in .env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

# Authentication Functions
def sign_up(email, password):
    """Sign up a new user"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if response.user:
            st.session_state.user = response.user
            return True, "Account created successfully!"
        return False, "Sign up failed"
    except Exception as e:
        return False, str(e)

def sign_in(email, password):
    """Sign in existing user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            st.session_state.user = response.user
            return True, "Logged in successfully!"
        return False, "Login failed"
    except Exception as e:
        return False, str(e)

def sign_out():
    """Sign out current user"""
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.session_state.chat_session = model.start_chat(history=[])
        return True
    except Exception as e:
        st.error(f"Logout error: {str(e)}")
        return False

# Supabase Functions
def create_new_session(user_id):
    """Create a new chat session"""
    try:
        response = supabase.table('chat_sessions').insert({
            'title': 'New Chat',
            'user_id': user_id
        }).execute()
        
        if response.data:
            return response.data[0]['id']
    except Exception as e:
        st.error(f"Error creating session: {str(e)}")
    return None

def save_message(session_id, role, content):
    """Save a message to Supabase"""
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

def load_user_sessions(user_id):
    """Load all chat sessions for current user"""
    try:
        response = supabase.table('chat_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
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
    try:
        supabase.table('chat_sessions')\
            .update({'title': title[:50]})\
            .eq('id', session_id)\
            .execute()
    except Exception as e:
        st.error(f"Error updating title: {str(e)}")

def delete_session(session_id):
    """Delete a chat session"""
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
    .auth-container {{
        max-width: 400px;
        margin: 5rem auto;
        padding: 2rem;
        background-color: {colors['secondary_bg']};
        border-radius: 12px;
        color: {colors['text']};
    }}
</style>
""", unsafe_allow_html=True)

# ============ AUTHENTICATION UI ============
if not st.session_state.user:
    st.markdown(f"""
    <div class="auth-container">
        <h1 style="text-align: center; color: {colors['accent']};">Welcome to Chat Assistant</h1>
        <p style="text-align: center; opacity: 0.7;">Please login or create an account</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if email and password:
                    success, message = sign_in(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter both email and password")
    
    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_signup = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit_signup:
                if new_email and new_password and confirm_password:
                    if new_password == confirm_password:
                        success, message = sign_up(new_email, new_password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords don't match")
                else:
                    st.warning("Please fill all fields")
    
    st.stop()  # Don't show chat if not logged in

# ============ MAIN CHAT UI (After Login) ============

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user.email}")
    
    if st.button("🚪 Logout", use_container_width=True):
        if sign_out():
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💬 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.current_session_id = None
        st.rerun()
    
    st.markdown("---")
    
    # Load user's sessions
    sessions = load_user_sessions(st.session_state.user.id)
    
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

# Header with theme toggle
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
        if not st.session_state.current_session_id:
            st.session_state.current_session_id = create_new_session(st.session_state.user.id)
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Save to Supabase
        if st.session_state.current_session_id:
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
            if st.session_state.current_session_id:
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