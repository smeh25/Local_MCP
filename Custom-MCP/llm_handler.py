import requests

def suggest_command_from_natural_language(query: str) -> str:
    payload = {
        "model": "mistral",  # or llama2, codellama, etc.
        "prompt": (
            "You are a command line assistant. "
            "Translate the user's request into a Linux shell command. "
            "Output only the command, nothing else.\n"
            f"{query}"
        ),
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    command = response.json().get("response", "").strip()
    return command
