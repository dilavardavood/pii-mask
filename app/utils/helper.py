import json
import os
import re

current_path = os.path.dirname(os.path.abspath(__file__))

base_path = os.path.dirname(current_path)  # go up to app/
kb_path = os.path.join(base_path, "knowledge_base")

def load_json_from_file(folder, filename):

    full_path = os.path.join(kb_path, folder, f"{filename}.json")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_json(response: str):
    try:
        # Extract content inside ```json ... ```
        match = re.search(r"```json\s*(.*?)```", response, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = response.strip()  # fallback in case no code block

        return json.loads(json_str)

    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {e}")