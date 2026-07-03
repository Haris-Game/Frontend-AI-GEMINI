import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="Haris Gemini", 
    page_icon="😎", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inject Custom CSS for Gemini Look & Feel
st.markdown("""
    <style>
        /* Global Background styling */
        .stApp {
            background-color: #131314;
            color: #e3e3e3;
        }
        
        /* Modernized Title styling */
        .gemini-title {
            font-size: 2.8rem;
            font-weight: 500;
            background: linear-gradient(45deg, #4285F4, #9B72CB, #D96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            font-family: 'Google Sans', sans-serif;
        }
        
        .gemini-subtitle {
            color: #80868b;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        /* Customize Streamlit native chat bubbles to feel more like Gemini */
        div[data-testid="stChatMessage"] {
            background-color: transparent !important;
            padding: 1rem 0rem !important;
            border-bottom: 1px solid #202124;
        }

        /* Give the User bubble a distinct subtle background alignment */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="user"]) {
            background-color: #1e1f20 !important;
            padding: 1rem !important;
            border-radius: 12px;
            border-bottom: none;
            margin-bottom: 0.5rem;
        }

        /* Input Container styling overrides */
        div[data-testid="stChatInput"] {
            border: 1px solid #3c4043 !important;
            border-radius: 30px !important;
            background-color: #1e1f20 !important;
            padding: 4px 12px !important;
        }
        
        div[data-testid="stChatInput"] textarea {
            color: #e3e3e3 !important;
            background-color: transparent !important;
        }
        
        /* Loading Spinner Color adjustment */
        div[data-testid="stSpinner"] i {
            color: #a87ffb !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Gemini Header
st.markdown('<h1 class="gemini-title">Hello, Whats Going On?</h1>', unsafe_allow_html=True)
st.markdown('<p class="gemini-subtitle">How can I help you discover or create today?</p>', unsafe_allow_html=True)
st.markdown("---")

BACKEND_URL = "https://angriness-theft-boggle.ngrok-free.dev/chat"

# 4. Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = "default_user_session"

# 5. Display chat history with updated custom avatars
for message in st.session_state.messages:
    # Use distinct emoji icons mimicking user/assistant states
    avatar = "👤" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. User Input Prompt
if user_query := st.chat_input("Ask Anything..."):
    
    # Render user input bubble immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)
        
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Render assistant response container
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        
        with st.spinner(""):
            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "message": user_query
                }
                
                response = requests.post(BACKEND_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    backend_data = response.json()
                    ai_reply = backend_data.get("reply", backend_data.get("response", "No response text found."))
                    
                    response_placeholder.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                else:
                    try:
                        error_detail = response.json().get("detail", "Unknown server error.")
                    except:
                        error_detail = response.text
                    st.error(f"⚠️ Server Error ({response.status_code}): {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Backend server is offline. Run 'uv run backend.py' first.")