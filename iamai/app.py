import streamlit as st
import google.generativeai as genai
# from key import api_key

# Load from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
email = st.secrets["SMTP_EMAIL"]
password = st.secrets["SMTP_PASSWORD"]

from inst import system_instruction



# Streamlit page setup
st.set_page_config(page_title="Flexing Data AI Chatbot", layout="wide")
st.title("🤖 Flexing Data's AI Chatbot")
st.markdown("Ask me anything about **Flexing Data's Data Analytics Internship Program!**")

# Configure Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"🧑‍💼 **{sender}:** {message}")
    else:
        st.markdown(f"🤖 **{sender}:** {message}")

# Chat input form (Enter-to-send enabled)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Type your question and press Enter...")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    try:
        # Append user input
        st.session_state.messages.append(("You", user_input.strip()))

        # Generate response from Gemini
        response = model.generate_content(user_input.strip())
        bot_reply = response.text.strip()

        # Append bot reply
        st.session_state.messages.append(("Bot", bot_reply))

        # Rerun to show updated chat
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")
