from core.llm import get_llm
from core.utils.json_utils import extract_json, parse_json_safe
from core.utils.retry import retry_llm_call

llm = get_llm()

ROUTER_PROMPT = """
You are an AI decision engine.

Choose ONE route:
- memory
- rag
- tool
- answer

Respond ONLY in JSON:

{{
  "route": "memory | rag | tool | answer"
}}

User Question:
{question}
"""


def route_with_llm(question):
    prompt = ROUTER_PROMPT.format(question=question)

    for response in retry_llm_call(llm, prompt):
        if not response:
            continue

        cleaned = extract_json(response)
        data = parse_json_safe(cleaned)

        route = data.get("route")

        if route:
            return route.strip().lower()

    # 🔥 FINAL FALLBACK
    return "answer"