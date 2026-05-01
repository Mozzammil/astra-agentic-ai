from core.llm import get_llm
from core.parser.json_parser import parse_json_safe
from core.retry.retry_llm import retry_llm_call

llm = get_llm()

def file_analyzer(content: str):
    prompt = f"""
You are a senior analyst.

Return STRICT JSON ONLY:

{{
  "summary": "short summary",
  "key_points": ["point1", "point2"],
  "insights": ["insight1", "insight2"]
}}

Content:
{content}
"""

    for response in retry_llm_call(llm, prompt):
        data = parse_json_safe(response)

        if data:
            return data

    return {"error": "Invalid JSON from LLM"}