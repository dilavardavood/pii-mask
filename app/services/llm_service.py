import requests
from app.config import Config

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def ask_openai(system_prompt, user_prompt, temperature=0.0):
    headers = {
        "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    data = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(OPENAI_URL, headers=headers, json=data)
    if response.ok:
        response_json = response.json()
        extracted_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return extracted_content
    else:
        print(f"OpenAI API error: {response.status_code} - {response.text}")
        return "Error: Unable to generate response."


def generate_openai(system_prompt, message, temperature=0.0):
    headers = {
        "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Base messages with system prompt
    messages = [{"role": "system", "content": system_prompt}, {
        "role": "user",
        "content": f"Content: '{message}'."
    }]

    # Add the actual user query

    data = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(OPENAI_URL, headers=headers, json=data)
    if response.ok:
        response_json = response.json()
        extracted_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return extracted_content
    else:
        print(f"OpenAI API error: {response.status_code} - {response.text}")
        return "Error: Unable to generate response."
