import streamlit as st
import google.generativeai as genai
from inst import system_instruction

# Secure secrets
api_key = st.secrets["GEMINI_API_KEY"]
email = st.secrets["SMTP_EMAIL"]
password = st.secrets["SMTP_PASSWORD"]

# Page config for popup style
st.set_page_config(
    page_title="Flexing Data AI Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Configure Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Custom CSS for polished UI
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f4f6f9;
}

.chat-title {
    text-align: center;
    font-size: 20px;
    color: #FF5722;
    margin-top: 10px;
    margin-bottom: 0;
}

.chat-subtitle {
    text-align: center;
    font-size: 14px;
    margin-bottom: 20px;
    color: #555;
}

.chat-bubble {
    padding: 10px 16px;
    border-radius: 16px;
    margin: 6px 0;
    max-width: 85%;
    line-height: 1.5;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    word-wrap: break-word;
    font-size: 14px;
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
</style>
""", unsafe_allow_html=True)

# Titles
st.markdown("<h3 class='chat-title'>🤖 Flexing Data AI Chatbot</h3>", unsafe_allow_html=True)
st.markdown("<p class='chat-subtitle'>Ask anything about our Data Analytics Internship Program</p>", unsafe_allow_html=True)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.messages:
    bubble_class = "user-bubble" if sender == "You" else "bot-bubble"
    role_icon = "🧑‍💼" if sender == "You" else "🤖"
    st.markdown(
        f'<div class="chat-bubble {bubble_class}">{role_icon} <strong>{sender}:</strong><br>{message}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# Chat input (Enter-to-send works perfectly)
user_input = st.chat_input("Type your message here...")

if user_input:
    user_input = user_input.strip()

    if len(user_input) > 1000:
        st.warning("Your message is too long. Please shorten it.")
    else:
        try:
            # Append user message
            st.session_state.messages.append(("You", user_input))

            # Generate Gemini response
            with st.spinner("Thinking..."):
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()

            st.session_state.messages.append(("Bot", bot_reply))

        except Exception as e:
            st.error("Something went wrong while generating a response.")
            st.exception(e)