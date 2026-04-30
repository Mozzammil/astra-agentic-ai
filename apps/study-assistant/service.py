from core.llm import get_llm
from core.parser import extract_json, parse_json
from core.retry import retry_llm_call
from core.validator import validate_study_response
from core.tools.calculator import calculator
from core.tools.summarizer import summarizer
from prompts import build_prompt

llm = get_llm()

def ask(question):
    prompt = build_prompt(question)

    for response in retry_llm_call(llm, prompt):
        print("RAW:", response)  # debug

        cleaned = extract_json(response)
        data = parse_json(cleaned)

        if not data:
            continue

        action = data.get("action")

        # 🔥 TOOL ROUTING
        if action == "calculator":
            return calculator(data.get("input"))

        if action == "summarizer":
            return summarizer(data.get("input"))

        if action == "answer" and validate_study_response(data):
            return data

    return {"error": "failed"}