# Plaksha-MS-AI-LAB1
LAB 1 PYTHON

Here is a complete, ready-to-use `README.md` file tailored specifically to your project requirements and grading rubric.

```markdown
# API Explorer — CLI Chatbot

A Python command-line chatbot interface powered by NVIDIA's NIM API (`meta/llama-3.1-8b-instruct`). It features full conversation persistence across restarts and robust error handling for missing credentials, loss of network connectivity, invalid inputs, and file corruption.

---

## Features

- **LLM Integration:** Connects seamlessly to NVIDIA's OpenAI-compatible endpoint.
- **Conversation Persistence:** Automatically saves your chat history to `conversations/history.json` on exit and reloads it upon startup.
- **Resilient Error Handling:**
  - Detects missing or unconfigured API keys immediately on launch.
  - Handles network disconnects, HTTP errors, and API rate limits (`429`) gracefully without crashing the application.
  - Recovers from missing or corrupted history JSON files by falling back to a clean state.
  - Ignores empty user inputs to prevent wasteful API requests.
- **Clean State Management:** Unsuccessful user messages are rolled back if an API call fails, keeping your saved history clean.

---

## Setup & Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Environment Setup
Clone this repository and set up a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

Install the required dependencies:

```bash
pip install -r requirements.txt

```

*(Your `requirements.txt` should contain `requests` and `python-dotenv`.)*

### 3. API Key Configuration

1. Obtain an API key from [NVIDIA Build](https://build.nvidia.com/settings/api-keys).
2. Create a `.env` file in the root directory of the project (ensure `.env` is listed in your `.gitignore` file):

```env
NVIDIA_API_KEY="nvapi-your-actual-key-here"

```

---

## Usage

Run the main script from your terminal:

```bash
python chatbot.py

```

### Controls

* Type your message and press **Enter** to chat.
* Type `quit` or `exit` to end the chat session and save your conversation history.
* Press **Ctrl+C** at any time to safely terminate the program.

---

## File Structure

```
.
├── chatbot.py            # Main application script
├── conversations/
│   └── history.json      # Saved conversation history (auto-generated)
├── .env                  # Local environment variables (DO NOT COMMIT)
├── .gitignore            # Git ignore file excluding .env
├── README.md             # Project documentation
└── requirements.txt      # Dependencies

```

---

## Error Handling Testing Matrix

| Test Case | How to Test | Expected Behavior |
| --- | --- | --- |
| **Missing API Key** | Remove or comment out `NVIDIA_API_KEY` in `.env` | Program outputs a clear message indicating missing credentials and exits cleanly. |
| **Network Failure / Rate Limits** | Disconnect Wi-Fi mid-conversation | Program prints a user-friendly error message, discards the pending turn, and allows you to continue once reconnected. |
| **Corrupted History File** | Edit `conversations/history.json` into invalid JSON | Program issues a warning, discards corrupted state, and initializes a fresh conversation. |
| **Empty Input** | Press Enter on an empty prompt | Program alerts the user that the message cannot be empty and re-prompts without calling the API. |

```

```
