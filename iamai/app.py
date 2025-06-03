import streamlit as st
import google.generativeai as genai
from inst import system_instruction
from datetime import datetime

# Secure credentials
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Page config
st.set_page_config(page_title="Flexing Data AI Chatbot", layout="centered")

# Custom CSS
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

st.markdown("<h3 style='text-align: center; color: #FF5722;'>🤖 Flexing Data AI Chatbot</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything about our Data Analytics Internship Program</p>", unsafe_allow_html=True)

# Ask user info once
if "user_info" not in st.session_state:
    with st.form("user_info_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        whatsapp = st.text_input("WhatsApp Number")
        submit = st.form_submit_button("Start Chat")
        if submit:
            if name and email and whatsapp:
                st.session_state.user_info = {
                    "name": name.strip(),
                    "email": email.strip(),
                    "whatsapp": whatsapp.strip(),
                }

                # Save user info
                with open("user_data.txt", "a", encoding="utf-8") as f:
                    f.write("\n" + "=" * 50 + "\n")
                    f.write(f"Name: {name}\nEmail: {email}\nWhatsApp: {whatsapp}\n")
                    f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("Chat Transcript:\n")
            else:
                st.warning("Please fill out all fields to start chatting.")
                st.stop()
        else:
            st.stop()

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    user_name = st.session_state.user_info["name"]
    st.session_state.messages.append(("You", user_input))

    # Call Gemini
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = "⚠️ Sorry, something went wrong."
            st.error(str(e))

    st.session_state.messages.append(("Bot", bot_reply))

    # Append to file
    with open("user_data.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%H:%M:%S")
        f.write(f"[{timestamp}] {user_name} ➤ {user_input}\n")
        f.write(f"[{timestamp}] Bot ➤ {bot_reply}\n")

# Display messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.messages:
    bubble_class = "user-bubble" if sender == "You" else "bot-bubble"
    role_icon = "🧑‍💼" if sender == "You" else "🤖"
    st.markdown(
        f'<div class="chat-bubble {bubble_class}">{role_icon} <strong>{sender}:</strong><br>{message}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)
