# 🤖 AI Chatbot with OpenRouter

A multi-model AI chatbot application that allows users to interact with various AI models through a clean and intuitive interface. Built with Python, Flask, and Streamlit.

![Application Interface](https://i.gyazo.com/84dcd63b8016a563bfd7f12392d74a7c.png)

## 📖 What is This?

This is a conversational AI chatbot application that enables users to:
- Chat with multiple AI models from different providers
- Maintain conversation history across multiple turns
- Switch between different AI models on the fly
- Save preferences locally for convenience

The application acts as a bridge between users and the OpenRouter API, providing an easy-to-use interface for accessing various large language models (LLMs) without needing to manage multiple API keys or platforms.

## 🏗️ How It Works

The application follows a **client-server architecture**:

1. **Frontend (Streamlit)**: 
   - Provides the user interface
   - Manages conversation history in session state
   - Handles user authentication and model selection
   - Displays messages in a chat format

2. **Backend (Flask)**:
   - Acts as a proxy to the OpenRouter API
   - Loads user configuration (API key, username, model)
   - Forwards conversation history to the selected AI model
   - Returns AI responses to the frontend

3. **Data Flow**:
   ```
   User Input → Frontend (Streamlit) → Backend (Flask) → OpenRouter API → AI Model
   AI Response ← Frontend ← Backend ← OpenRouter API ← AI Model
   ```

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Frontend framework for building the web interface
- **Flask**: Backend web framework for API handling
- **Flask-CORS**: Enables cross-origin requests between frontend and backend
- **Requests**: HTTP library for making API calls to OpenRouter
- **OpenRouter API**: Gateway to access multiple AI models

## 🌐 What is OpenRouter?

[OpenRouter](https://openrouter.ai/) is a unified API platform that provides access to multiple AI models from various providers through a single interface. Instead of managing separate API keys and integrations for OpenAI, Anthropic, Google, Meta, and others, OpenRouter consolidates them all.

**Benefits**:
- Access to 100+ AI models (GPT-4, Claude, Llama, Gemini, etc.)
- Single API key for all models
- Pay-per-use pricing
- Good availability of free models
- Automatic model routing and fallbacks
- No need for multiple subscriptions

## 🔑 How to Get an OpenRouter API Key

1. **Visit OpenRouter**: Go to [https://openrouter.ai/](https://openrouter.ai/)

2. **Sign Up**: Click on "Sign In" and create an account using:
   - Google account
   - GitHub account
   - Email address

3. **Generate API Key**:
   - Go to "API Keys" section in your dashboard
   - Click "Create Key"
   - Copy your API key (it starts with `sk-or-v1-...`)
   - **Important**: Save it securely, you won't be able to see it again!

4. **Add Credits** (Optional but recommended): 
   - Navigate to your account dashboard
   - Go to the "Credits" section
   - Add funds to your account (start with $5-$10 for testing)

5. **Set Usage Limits** (Optional but recommended):
   - Set spending limits to control costs
   - Enable email notifications for usage alerts

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher installed
- Git installed
- Terminal/Command Prompt access

### Step 1: Clone the Repository

```bash
git clone https://github.com/Stareg66/Chatbot
cd Chatbot
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If `requirements.txt` doesn't exist, create it with the following content:
```
flask==3.0.0
flask-cors==4.0.0
streamlit==1.29.0
requests==2.31.0
```

Then run the install command again.

### Step 4: Run the Backend Server

Open a terminal window and run:

```bash
python backend.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Keep this terminal window open** - the backend must be running for the chatbot to work.

### Step 5: Run the Frontend Application

Open a **second terminal window** (keep the backend running) and run:

```bash
streamlit run front.py
```

Your default web browser should automatically open to `http://localhost:8501`

If it doesn't open automatically, manually navigate to the URL shown in the terminal.

![Application Interface](https://i.gyazo.com/336e9727c9ed1c49cdc9898cac4f8f4b.png)

## 📝 Using the Application

### First Time Setup

1. **Enter Your Information**:
   - In the sidebar, enter your username
   - Paste your OpenRouter API key
   - Click "💾 Save"

2. **Select a Model**:
   - After saving, a model dropdown will appear
   - Choose your preferred AI model (e.g., `openai/gpt-4`, `anthropic/claude-3.5-sonnet`)
   - The selection is automatically saved

3. **Start Chatting**:
   - Type your message in the chat input at the bottom
   - Press Enter or click Send
   - The AI will respond with context from your conversation history

### Features

- **💬 Multi-turn Conversations**: The bot remembers previous messages in the current session
- **🔄 Model Switching**: Change AI models mid-conversation
- **🗑️ Clear Conversation**: Reset your chat history at any time
- **💾 Persistent Settings**: Your API key, username, and model preference are saved locally
- **🔒 Secure**: API key is stored locally and never shared

## 📁 Project Structure

```
ai-chatbot/
│
├── backend.py          # Flask server handling API requests
├── front.py            # Streamlit frontend interface
├── requirements.txt    # Python dependencies
├── userconfig.json     # Auto-generated config file (not in git)
└── README.md          # This file
```

## 🔧 Configuration

The application automatically creates a `userconfig.json` file to store:
- Your OpenRouter API key
- Username
- Selected model

## 🐛 Troubleshooting

### Backend Won't Start
- **Error**: `Address already in use`
- **Solution**: Another application is using port 5000. Kill that process or change the port in `backend.py`

### Frontend Can't Connect to Backend
- **Error**: `Failed to reach backend`
- **Solution**: Make sure `backend.py` is running in a separate terminal window

### API Key Invalid
- **Error**: `Missing API key, username, or model in configuration`
- **Solution**: Re-enter your API key in the sidebar and ensure it starts with `sk-or-v1-`

### Model Not Loading
- **Error**: `Failed to load models`
- **Solution**: Check your API key validity and internet connection

## 💡 Tips for Best Results

- **Choose the right model**: Faster models like GPT-3.5 are good for simple tasks, while GPT-4, Claude or GLM-4 are better for complex reasoning.
- **Be specific**: Clear, detailed prompts get better responses.
- **Use conversation history**: The bot remembers context, so you can refer to previous messages.
- **Use free models**: A great number of free models are available for use. Check the privacy configuration of your OpenRouter account and try them.
- **Monitor costs**: Check your OpenRouter dashboard regularly to track spending.

## 🚧 Roadmap

### Version 1.1 (Coming Soon)

- **🗂️ Multi-Conversation Management**: Create and manage multiple independent chat sessions
- **⚙️ Custom System Prompts**: Customize the AI's behavior and personality for each conversation
- **💾 Local Storage**: All conversations saved locally for easy access

### Version 1.2 (Planned)

- **🎛️ Advanced Generation Parameters**: Control AI output with adjustable settings:
  - Temperature (creativity vs consistency)
  - Top-K (vocabulary diversity)
  - Top-P (nucleus sampling)
  - Max tokens (response length)
  - Frequency/presence penalties
- **💳 Credit Balance Checker**: View your current OpenRouter API credits with a single button click directly in the app

Stay tuned for updates!


## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ by Manuel Rueda Algar

---

**Questions or Issues?** Open an issue on GitHub or contact the maintainer.

