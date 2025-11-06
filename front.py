import streamlit as st
import requests
import json
import os

CONFIG_FILE = "userconfig.json"

def save_config(api_key=None, username=None, model=None):
    "Save API key, username and model to local config file."
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

def load_config():
    "Load API key, username and model from config file."
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def clear_config():
    "Delete local config file."
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

# Page Config
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

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
st.write("Explore with the different OpenRouter models!")

# Sidebar
with st.sidebar:

    st.header("⚙️ Settings")

    # --- API & User Key management ---
    if "api_key" not in st.session_state:
        username_input = st.text_input("👤 Username:", value=st.session_state.get("username", ""))
        api_key_input = st.text_input("🔑 OpenRouter API key:", type="password")
        if st.button("💾 Save"):
            if api_key_input.strip():
                # Save both username and API key
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
            st.rerun()

    # --- Model selection (only after key is set) ---
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
