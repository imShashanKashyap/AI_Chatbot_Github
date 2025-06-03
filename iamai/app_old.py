import streamlit as st
import google.generativeai as genai
from inst import system_instruction

# Load secure credentials from secrets
api_key = st.secrets["GEMINI_API_KEY"]
email = st.secrets["SMTP_EMAIL"]
password = st.secrets["SMTP_PASSWORD"]

# Page config
st.set_page_config(page_title="Flexing Data AI Chatbot", layout="wide")
st.title("🤖 Flexing Data's AI Chatbot")
st.markdown("Ask me anything about **Flexing Data's Data Analytics Internship Program!**")

# Configure Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for sender, message in st.session_state.messages:
    role_icon = "🧑‍💼" if sender == "You" else "🤖"
    st.markdown(f"{role_icon} **{sender}:** {message}")

# Chat form with enter-to-send
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Type your question and press Enter...")
    submitted = st.form_submit_button("Send")

# Process message
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

            # Generate Gemini response
            with st.spinner("Thinking..."):
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()

            st.session_state.messages.append(("Bot", bot_reply))

            # Guard rerun to avoid infinite redirect
            if "safe_rerun" not in st.session_state:
                st.session_state.safe_rerun = True
                st.rerun()

        except Exception as e:
            st.error("Something went wrong while generating a response.")
            st.exception(e)
