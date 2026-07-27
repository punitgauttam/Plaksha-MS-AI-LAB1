"""
history.py — load and save conversation history as JSON.
"""

import json
from pathlib import Path

DEFAULT_HISTORY_PATH = Path("conversations/history.json")

DEFAULT_SYSTEM_PROMPT = [
    {"role": "system", "content": "You are a helpful, concise assistant."}
]


def load_history(path: Path, system_prompt=None):
    """
    Load a saved conversation from `path`.

    Target 3: Corrupted or missing conversation JSON file on load.
    - If the file doesn't exist, start a fresh conversation (no warning needed,
      that's the normal first run).
    - If the file exists but can't be parsed, or isn't the shape we expect,
      warn the user and start fresh rather than crashing.
    """
    system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    if not path.exists():
        print("No saved conversation found — starting fresh.")
        return list(system_prompt)

    try:
        with open(path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        print(f"[Warning] Couldn't read '{path}' ({e}). Starting a fresh conversation instead.")
        return list(system_prompt)

    if not isinstance(messages, list) or not all(
        isinstance(m, dict) and "role" in m and "content" in m for m in messages
    ):
        print(f"[Warning] '{path}' doesn't look like a valid conversation. Starting fresh.")
        return list(system_prompt)

    print(f"Loaded existing conversation from '{path}' ({len(messages)} messages).")
    return messages


def save_history(path: Path, messages):
    """Save the full conversation to `path`, creating parent folders as needed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2)
        print(f"Conversation saved to '{path}'.")
    except OSError as e:
        print(f"[Warning] Failed to save conversation: {e}")
