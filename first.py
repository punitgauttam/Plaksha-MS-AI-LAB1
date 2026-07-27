"""
chatbot.py — entry point. Wires together llm.py and history.py into a
command-line chatbot that remembers the conversation across restarts.
"""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from llm import call_model, get_api_key
from history import load_history, save_history, DEFAULT_HISTORY_PATH

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="A little chatbot with memory.")
    parser.add_argument(
        "--system",
        help="Custom system prompt to use when starting a NEW conversation "
        "(ignored if a saved conversation is being loaded).",
    )
    parser.add_argument(
        "--load",
        help="Path to a specific saved conversation JSON file to resume.",
    )
    parser.add_argument(
        "--save",
        help="Path to save the conversation to (defaults to the --load path, "
        "or conversations/history.json).",
    )
    return parser.parse_args()


def run_chat(history_path: Path, save_path: Path, system_prompt):
    # Target 1: fail fast, before doing anything else, if the key is missing.
    api_key = get_api_key()

    messages = load_history(history_path, system_prompt=system_prompt)

    print("\n--- Chat started. Type 'quit' to stop. ---")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nInterrupted — saving and exiting.")
            break

        # Target 4: empty input just re-prompts, no API call.
        if not user_input:
            print("(Type something before hitting enter.)")
            continue

        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})
        reply = call_model(messages, api_key)

        if reply is None:
            # The call failed — don't leave a user turn with no reply in the
            # saved history, so the conversation stays sensible on disk.
            messages.pop()
            print("(That message wasn't sent — you can try again.)")
            continue

        messages.append({"role": "assistant", "content": reply})
        print(f"\nAssistant: {reply}")

    save_history(save_path, messages)
    print("Goodbye!")


def main():
    args = parse_args()

    history_path = Path(args.load) if args.load else DEFAULT_HISTORY_PATH
    save_path = Path(args.save) if args.save else history_path

    system_prompt = None
    if args.system:
        system_prompt = [{"role": "system", "content": args.system}]

    run_chat(history_path, save_path, system_prompt)


if __name__ == "__main__":
    main()
