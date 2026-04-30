import json
import re

def extract_json(text):
    """
    Extract JSON object from LLM response.
    Handles cases where model adds extra text.
    """
    if not text:
        return text

    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def parse_json(text):
    """
    Convert string → JSON safely
    """
    try:
        return json.loads(text)
    except Exception:
        return None


def validate_response(data):
    """
    Validate expected schema for Study Assistant
    """
    if not data:
        return False

    required_keys = ["question", "answer", "summary"]

    for key in required_keys:
        if key not in data or not data[key]:
            return False

    return True