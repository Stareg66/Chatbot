import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

# Header 
st.title("🚀 AI Chatbot")
st.write("Explore the different OpenRouter models")

# Sidebar
st.sidebar.title("Settings")
name = st.sidebar.text_input("Enter your name:", "User")

# Main Interaction
st.header("Main Interaction")
user_input = st.text_input("Type something:", "")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message first.")
    else:
        # Send POST request to backend
        try:
            response = requests.post(
                "http://127.0.0.1:5000/chat",
                json={"message": user_input}
            )
            if response.status_code == 200:
                data = response.json()
                st.success(f"Response: {data['reply']}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to reach backend: {e}")

# Footer
st.markdown("---")
st.caption("Built with Streamlit and Python by Manuel Rueda Algar")
