import streamlit as st
import google.generativeai as genai
import time
import os
from PIL import Image
import base64
from io import BytesIO

# --- User Credentials ---
VALID_USERS = {"Shahid Khan": "sk2140"}

# --- Page Config ---
st.set_page_config(page_title="AthenaAI 2.0", page_icon="logo.png", layout="wide")

# --- Render Circular Logo ---
def render_logo_base64(path, size=100):
    if not os.path.exists(path):
        return
    img = Image.open(path).resize((size, size))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; padding: 10px;">
            <img src="data:image/png;base64,{img_b64}"
                 style="border-radius: 50%; width: {size}px; height: {size}px; object-fit: cover;
                        background-color: transparent; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Login Page ---
def login():
    st.title("AthenaAI 2.0 Login")
    st.write("Welcome to your personal AI assistant. Please log in.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

# --- Welcome Banner ---
def welcome_banner():
    st.markdown(
        f"""
        <div style="background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
                    padding: 20px; border-radius: 16px; color: white; text-align: center;">
            <h1>Welcome, <strong>{st.session_state.username}</strong></h1>
            <p>I’m <strong>AthenaAI 2.0</strong> — your personal AI assistant powered by Gemini & Shahid Khan</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Save & Load Chat History ---
def save_user_history(username, user_input, ai_response):
    with open(f"history_{username}.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_input}\nAthenaAI: {ai_response}\n{'-'*50}\n")

def load_user_history(username):
    try:
        with open(f"history_{username}.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No previous chats found."

# --- Chat Application ---
def run_app():
    with st.sidebar:
        render_logo_base64("logo.png", size=100)
        st.markdown("<h4 style='text-align: center; margin-top: 0;'>AthenaAI</h4>", unsafe_allow_html=True)

        st.markdown("### Configuration")
        api_key = st.text_input("Google API Key", type="password")

        st.markdown("---")
        st.markdown("### Chat Controls")

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        if "show_history" not in st.session_state:
            st.session_state.show_history = False

        if st.button("Show Chat History" if not st.session_state.show_history else "Hide Chat History"):
            st.session_state.show_history = not st.session_state.show_history

        if st.session_state.show_history:
            history = load_user_history(st.session_state.username)
            st.text_area("Chat History", value=history, height=300, disabled=True)

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # --- API Setup ---
    if not api_key:
        st.warning("Please enter your Google API key to continue.")
        st.stop()

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction="You are AthenaAI 2.0, a helpful, professional, and warm assistant."
        )
    except Exception as e:
        st.error(f"API Error: {e}")
        st.stop()

    # --- Main Panel ---
    welcome_banner()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I’m AthenaAI 2.0. How can I help you today?"}
        ]

    # Display messages (no avatars)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=None):
            st.markdown(msg["content"])

    # Handle user input
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=None):
            placeholder = st.empty()
            full_response = ""
            try:
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt, stream=True)
                for chunk in response:
                    full_response += chunk.text or ""
                    placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)
                placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"Error: {e}"
                placeholder.error(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_user_history(st.session_state.username, prompt, full_response)

# --- Launch App ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    run_app()
