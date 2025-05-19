import streamlit as st
import requests
import os
import signal

# Find and kill process using port 8000
!ps -fA | grep uvicorn

# If any uvicorn process is running, kill it
for line in os.popen("lsof -i :8000"):
    if "LISTEN" in line:
        pid = int(line.split()[1])
        print(f"Killing process {pid} on port 8000")
        os.kill(pid, signal.SIGKILL)


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
 
