import json

def parse_json_safe(text):
    try:
        return json.loads(text)
    except Exception:
        return None