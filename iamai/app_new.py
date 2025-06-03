import streamlit as st
import google.generativeai as genai
from inst import system_instruction

# Secure secrets
api_key = st.secrets["GEMINI_API_KEY"]
email = st.secrets["SMTP_EMAIL"]
password = st.secrets["SMTP_PASSWORD"]

# Configure page
st.set_page_config(page_title="Flexing Data AI Chatbot", layout="centered")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Custom styling
st.markdown("""
<style>
.chat-bubble {
    padding: 10px 16px;
    border-radius: 16px;
    margin: 6px 0;
    max-width: 85%;
    line-height: 1.5;
    font-size: 14px;
    word-wrap: break-word;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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
    max-height: 420px;
    overflow-y: auto;
    padding: 10px;
    background-color: #eaf1f8;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Heading
st.markdown("<h3 style='text-align: center; color: #FF5722;'>🤖 Flexing Data AI Chatbot</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask about our Data Analytics Internship Program</p>", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle user input
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append(("You", user_input))

    # Call Gemini and store response
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            reply = response.text.strip()
        except Exception as e:
            reply = "⚠️ Sorry, there was an error processing your request."
            st.error(str(e))

    st.session_state.messages.append(("Bot", reply))

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