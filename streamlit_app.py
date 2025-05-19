import streamlit as st
import requests

st.title("Islamic Chatbot")
session_id = st.session_state.get("session_id", "user123")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask your question:")

if st.button("Send") and user_input:
    payload = {"session": session_id, "message": user_input}
    response = requests.post("http://localhost:8000/chat", json=payload).json()
    st.session_state.chat.append(("User", user_input))
    st.session_state.chat.append(("Assistant", response["answer"]))

for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:** {message}")
 
