def validate_study_response(data):
    if not data:
        return False

    required_keys = ["question", "answer", "summary"]

    for key in required_keys:
        if key not in data or not data[key]:
            return False

    return True