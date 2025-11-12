import streamlit as st
import requests
import json
import os

CONFIG_FILE = "userconfig.json"

# Save API key, username and model to local config file.
def save_config(api_key=None, username=None, model=None):
   
    data = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}

    if api_key is not None:
        data["api_key"] = api_key
    if username is not None:
        data["username"] = username
    if model is not None:
        data["model"] = model

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

# Load API key, username and model from config file.
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Delete local config file.
def clear_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

# Page Config
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Load saved data on start
config_data = load_config()
if "api_key" not in st.session_state and "api_key" in config_data:
    st.session_state["api_key"] = config_data["api_key"]

if "username" not in st.session_state and "username" in config_data:
    st.session_state["username"] = config_data["username"]

if "selected_model" not in st.session_state and "model" in config_data:
    st.session_state["selected_model"] = config_data["model"]

# Header 
st.title("🚀 AI Chatbot")
st.write("Explore with different OpenRouter models!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # API & User Key management
    if "api_key" not in st.session_state:
        username_input = st.text_input("👤 Username:", value=st.session_state.get("username", ""))
        api_key_input = st.text_input("🔑 OpenRouter API key:", type="password")
        if st.button("💾 Save"):
            if api_key_input.strip():
                st.session_state["api_key"] = api_key_input.strip()
                st.session_state["username"] = username_input.strip()
                save_config(api_key_input.strip(), username_input.strip())
                st.success("Saved successfully!")
                st.rerun()
            else:
                st.warning("Please enter your API key.")
    else:
        st.success(f"✅ Logged in as {st.session_state.get('username', 'Unknown')}")
        if st.button("🗑️ Remove Key and User"):
            clear_config()  # remove from file
            st.session_state.pop("api_key", None)
            st.session_state.pop("username", None)
            st.session_state.pop("selected_model", None)
            st.session_state["messages"] = []  # Clear message history
            st.rerun()

    # Model selection (only after key is set)
    if "api_key" in st.session_state:
        st.markdown("---")
        st.subheader("🧠 Model Selection")
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {st.session_state['api_key']}"}
            )
            if response.status_code == 200:
                models_data = response.json()
                model_list = [m["id"] for m in models_data["data"]]
                # --- Model selection without key conflict ---
                default_model = (
                    st.session_state.get("selected_model")
                    if st.session_state.get("selected_model") in model_list
                    else model_list[0]
                )

                selected_model = st.selectbox(
                    "Choose a model:",
                    model_list,
                    index=model_list.index(default_model),
                )

                # Store and persist the new selection only if it changes
                if selected_model != st.session_state.get("selected_model"):
                    st.session_state["selected_model"] = selected_model
                    save_config(model=selected_model)
            else:
                st.error(f"Failed to load models:\n{response.text}")
        except Exception as e:
            st.error(f"Error fetching models: {e}")     

        # Clear conversation button
        st.markdown("---")
        if st.button("🗑️ Clear Conversation"):
            st.session_state["messages"] = []
            st.rerun()


# Main Chat Interface
st.header("💬 Chat")

# Display conversation history
if st.session_state["messages"]:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])


# Chat input
if "api_key" in st.session_state:
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(user_input)

        # Send conversation history to backend
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={"messages": st.session_state["messages"]},
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                assistant_reply = data["reply"]
                
                # Add assistant response to history
                st.session_state["messages"].append({
                    "role": "assistant", 
                    "content": assistant_reply
                })
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.write(assistant_reply)
                
                st.rerun()
            else:
                try:
                    data = response.json()
                    st.error(f"Error: {data.get('error', f'Status {response.status_code}')}")
                except:
                    st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except Exception as e:
            st.error(f"Failed to reach backend: {e}")
else:
    st.info("👈 Please enter your API key in the sidebar to start chatting.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit and Python by Manuel Rueda Algar")
