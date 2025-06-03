import streamlit as st
import google.generativeai as genai
from inst import system_instruction

# Secure secrets
api_key = st.secrets["GEMINI_API_KEY"]
email = st.secrets["SMTP_EMAIL"]
password = st.secrets["SMTP_PASSWORD"]

# Page config (optimized for popup)
st.set_page_config(
    page_title="Flexing Data AI Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a beautiful chat look
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f4f6f9;
    }

    .chat-bubble {
        padding: 10px 16px;
        border-radius: 16px;
        margin: 6px 0;
        max-width: 85%;
        line-height: 1.5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }

    .user-bubble {
        background-color: #075E54;
        color: white;
        margin-left: auto;
    }

    .bot-bubble {
        background-color: #ffffff;
        color: #333;
        margin-right: auto;
        border: 1px solid #ccc;
    }

    .chat-container {
        max-height: 430px;
        overflow-y: auto;
        padding: 10px;
        background-color: #eaf1f8;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }

    .input-container {
        position: relative;
        margin-top: 10px;
    }

    input[type="text"] {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 10px;
    }

    </style>
""", unsafe_allow_html=True)

# Title area
st.markdown("<h3 style='text-align: center; color: #FF5722;'>🤖 Flexing Data AI Chatbot</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything about our Data Analytics Internship Program!</p>", unsafe_allow_html=True)

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in st.session_state.messages:
        bubble_class = "user-bubble" if sender == "You" else "bot-bubble"
        role_icon = "🧑‍💼" if sender == "You" else "🤖"
        st.markdown(
            f'<div class="chat-bubble {bubble_class}">{role_icon} <strong>{sender}:</strong><br>{message}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submitted = st.form_submit_button("Send")

# Handle input
if submitted:
    user_input = user_input.strip()

    if not user_input:
        st.warning("Please enter a message.")
    elif len(user_input) > 1000:
        st.warning("Your message is too long. Please shorten it.")
    else:
        try:
            # Append user message
            st.session_state.messages.append(("You", user_input))

            # Generate response
            with st.spinner("Thinking..."):
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()

            # Append bot message
            st.session_state.messages.append(("Bot", bot_reply))

        except Exception as e:
            st.error("Something went wrong while generating a response.")
            st.exception(e)
