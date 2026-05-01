import json
from core.llm import get_llm
from core.utils.json_utils import extract_json, parse_json_safe
from core.utils.retry import retry_llm_call

llm = get_llm()

PLANNER_PROMPT = """
You are an AI agent planner.

Break the user request into steps.

Available tools:
- file_reader
- file_analyzer
- summarizer
- calculator

Return ONLY JSON:

{{
  "steps": [
    {{"action": "tool_name", "input": "input"}}
  ]
}}

Rules:
- Use multiple steps if needed
- Keep actions logical
- Last step should produce final answer

User Question:
{question}
"""


def create_plan(question):
    prompt = PLANNER_PROMPT.format(question=question)

    for response in retry_llm_call(llm, prompt):
        if not response:
            continue

        cleaned = extract_json(response)
        data = parse_json_safe(cleaned)

        steps = data.get("steps")

        if steps and isinstance(steps, list):
            return steps

    return []