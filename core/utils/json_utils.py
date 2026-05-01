import re
import json

def extract_json(text):
    """
    Extract JSON from messy LLM response
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else "{}"


def parse_json_safe(text):
    """
    Safe JSON parsing with fallback
    """
    try:
        return json.loads(text)
    except:
        return {}