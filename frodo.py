import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


# ================ Initialize Streamlit =====================================
st.set_page_config(
    page_title="Ask Frodo",
    page_icon=":books:",
    layout="centered",
)

# Replace this with your actual channel token if not already done elsewhere
channel_token = "your_channel_token_here"
URL = f"https://payload.vextapp.com/hook/YT8U5QEG5K/catch/{channel_token}"

headers = {
    "Content-Type": "application/json",
    "Apikey": f"Api-Key {API_KEY}",
}


st.title("Lord Of The Rings")
# ================= # Initialize chat history # ========================== #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================ # React to user input # ====================== #
quest = st.chat_input("Ask me about my adventure...")


if quest:
    question = str(quest)
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # ==== Get response from db ======
        data = {"payload": question}
        response = requests.post(URL, headers=headers, json=data)
        response_json = response.json()
        answer = response_json.get("text", "I don't remember that.")

    with st.chat_message("assistant"):
        st.markdown(answer)
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
