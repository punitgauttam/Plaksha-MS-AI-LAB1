"""
llm.py — talks to the NVIDIA NIM (OpenAI-compatible) chat completions endpoint.

Only responsibility: given a full conversation (list of {"role", "content"}
messages), send it to the model and return the assistant's reply text.
No memory lives here — the caller is responsible for resending the full
history each time.
"""

import os
import requests

URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "meta/llama-3.1-8b-instruct"


def get_api_key():
    """
    Target 1: Missing or invalid API key.
    Reads NVIDIA_API_KEY from the environment and exits immediately with a
    clear message if it isn't set. Meant to be called once, before anything
    else runs (see chatbot.py).
    """
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key or not api_key.strip():
        print(
            "[Fatal] NVIDIA_API_KEY is not set.\n"
            "        Add it to a .env file in this folder, e.g.:\n"
            '        NVIDIA_API_KEY="nvapi-your-key-here"\n'
            "        or export it in your shell before running the program."
        )
        raise SystemExit(1)
    return api_key.strip()


def call_model(messages, api_key, timeout=30):
    """
    Send the full conversation so far to the model and return the reply text.

    Target 2: Dropped connection, timeout, or API error response (incl. 429s).
    A failed call returns None instead of raising, so the caller can keep the
    chat loop alive and let the user try again.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"model": MODEL, "messages": messages}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        print("[Error] The request timed out. The API may be slow right now — try again.")
    except requests.exceptions.ConnectionError:
        print("[Error] Couldn't connect. Check your internet connection and try again.")
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code if err.response is not None else "?"
        if status == 429:
            print("[Error] Rate limited (429) by the free tier. Wait a moment and try again.")
        elif status in (401, 403):
            print(f"[Error] Authentication failed ({status}). Check that your API key is valid.")
        else:
            print(f"[Error] API returned an error ({status}). Try again in a moment.")
    except requests.exceptions.RequestException as err:
        print(f"[Error] Request failed: {err}")
    except (KeyError, IndexError, ValueError):
        print("[Error] Got back a response in a shape we didn't expect. Try again.")

    return None
