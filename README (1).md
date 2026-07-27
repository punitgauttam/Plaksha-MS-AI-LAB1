# API Explorer

A command-line chatbot that talks to an LLM (NVIDIA NIM's OpenAI-compatible
endpoint, model `meta/llama-3.1-8b-instruct`), holds a real back-and-forth
conversation, and remembers that conversation across restarts by saving it
to a JSON file.

## Files

- `chatbot.py` — entry point; runs the chat loop and CLI flags.
- `llm.py` — sends the conversation to the model and returns the reply.
- `history.py` — loads and saves conversation history as JSON.
- `conversations/` — saved conversation JSON files live here.

## Setup

1. Get a free API key from [build.nvidia.com](https://build.nvidia.com)
   (Settings → API Keys). Verify your phone number first if you haven't.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your key to `.env` in this folder:
   ```
   NVIDIA_API_KEY="nvapi-your-key-here"
   ```
   Never commit this file — it's already in `.gitignore`.

## Running it

```
python chatbot.py
```

- Type a message and press enter to chat.
- Type `quit` to end the conversation. It's saved automatically to
  `conversations/history.json`.
- Run the program again and it picks up right where you left off.

### Optional flags

```
python chatbot.py --system "You are a sarcastic pirate."
python chatbot.py --load conversations/my_chat.json
python chatbot.py --save conversations/my_chat.json
```

- `--system` sets a custom system prompt, but only takes effect when starting
  a brand new conversation (it's ignored if a saved conversation is loaded).
- `--load` resumes a specific saved conversation file instead of the default.
- `--save` saves to a specific file instead of the `--load`/default path.

## Error handling

The program is designed to fail gracefully instead of crashing:

- **Missing/invalid API key** — checked before anything else runs; exits
  immediately with a clear message.
- **Network/API errors** (dropped connection, timeout, rate limits) — caught
  per-call; you see a readable error and can keep chatting.
- **Corrupted or missing `history.json`** — a warning is printed and the
  program starts a fresh conversation instead of crashing.
- **Empty input** — hitting enter with nothing typed just re-prompts; nothing
  is sent to the API.

If a model call fails partway through a turn, the user's message is removed
from the in-memory conversation before saving, so the saved JSON never ends
with a dangling question that never got answered.
