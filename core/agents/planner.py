import json

from core.llm import get_llm
from core.utils.retry import retry_llm_call
from core.utils.json_utils import (
    extract_json,
    parse_json_safe
)

llm = get_llm()

# ==================================================
# 🧠 PLANNER PROMPT
# ==================================================
PLANNER_PROMPT = """
You are an advanced AI planning agent.

Your task:
Create a minimal step-by-step execution plan.

You have access to these tools:

1. file_reader
   - Reads file content

2. summarizer
   - Summarizes text

3. file_analyzer
   - Extracts:
     - key points
     - insights
     - analysis

4. calculator
   - Solves mathematical expressions

==================================================

MEMORY CONTEXT:
{memory_context}

==================================================

RAG CONTEXT:
{rag_context}

==================================================

Rules:
- Use ONLY available tools
- Keep plan short
- Avoid unnecessary steps
- Use placeholders:
    <content>
    <summary>
    <analysis>
- Output ONLY valid JSON
- Never explain outside JSON

==================================================

JSON FORMAT:

{{
  "steps": [
    {{
      "action": "tool_name",
      "input": "tool_input",
      "reason": "why tool is needed"
    }}
  ]
}}

==================================================

User Question:
{question}
"""


# ==================================================
# 🚀 MAIN PLANNER
# ==================================================
def create_plan(
    question,
    memory_context="",
    rag_context=""
):
    try:

        prompt = PLANNER_PROMPT.format(
            question=question,
            memory_context=memory_context,
            rag_context=rag_context
        )

        # ==================================================
        # 🔁 RETRY LOOP
        # ==================================================
        for response in retry_llm_call(llm, prompt):

            if not response:
                continue

            print("\n🧠 RAW PLAN RESPONSE:")
            print(response)

            # ==================================================
            # 🔥 EXTRACT JSON
            # ==================================================
            cleaned_json = extract_json(response)

            print("\n🧹 CLEANED JSON:")
            print(cleaned_json)

            # ==================================================
            # 🔥 SAFE PARSE
            # ==================================================
            data = parse_json_safe(cleaned_json)

            print("\n🧠 PARSED PLAN:")
            print(data)

            # ==================================================
            # 🚫 INVALID JSON
            # ==================================================
            if not data:
                print("⚠️ Invalid planner JSON")
                continue

            # ==================================================
            # 🔥 EXTRACT STEPS
            # ==================================================
            steps = data.get("steps")

            if not steps:
                print("⚠️ No steps found")
                continue

            if not isinstance(steps, list):
                print("⚠️ Steps must be a list")
                continue

            # ==================================================
            # 🔥 VALIDATE STEP STRUCTURE
            # ==================================================
            valid_steps = []

            for step in steps:

                if not isinstance(step, dict):
                    continue

                action = step.get("action")
                action_input = step.get("input")
                reason = step.get("reason", "")

                if not action:
                    continue

                valid_steps.append({
                    "action": str(action).strip(),
                    "input": str(action_input),
                    "reason": str(reason)
                })

            # ==================================================
            # ✅ SUCCESS
            # ==================================================
            if valid_steps:
                return valid_steps

        # ==================================================
        # 🚫 FALLBACK
        # ==================================================
        print("⚠️ Planner failed → fallback plan")

        return fallback_plan(question)

    except Exception as e:

        print("❌ Planner crashed:", str(e))

        return fallback_plan(question)


# ==================================================
# 🛡️ FALLBACK PLAN
# ==================================================
def fallback_plan(question):

    q = question.lower()

    print("🛡️ Using fallback planner")

    # ==================================================
    # 🔥 FILE ANALYSIS
    # ==================================================
    if "analyze" in q and ".txt" in q:

        filename = extract_filename(question)

        return [
            {
                "action": "file_reader",
                "input": filename,
                "reason": "Read file before analysis"
            },
            {
                "action": "file_analyzer",
                "input": "<content>",
                "reason": "Analyze file content"
            }
        ]

    # ==================================================
    # 🔥 FILE SUMMARY
    # ==================================================
    if "summarize" in q and ".txt" in q:

        filename = extract_filename(question)

        return [
            {
                "action": "file_reader",
                "input": filename,
                "reason": "Read file before summarization"
            },
            {
                "action": "summarizer",
                "input": "<content>",
                "reason": "Summarize file content"
            }
        ]

    # ==================================================
    # 🔥 CALCULATOR
    # ==================================================
    if any(op in q for op in ["+", "-", "*", "/"]):

        return [
            {
                "action": "calculator",
                "input": question,
                "reason": "Perform calculation"
            }
        ]

    # ==================================================
    # 🔥 DEFAULT FILE READ
    # ==================================================
    if ".txt" in q:

        filename = extract_filename(question)

        return [
            {
                "action": "file_reader",
                "input": filename,
                "reason": "Read file content"
            }
        ]

    # ==================================================
    # 🚫 NO PLAN
    # ==================================================
    return []


# ==================================================
# 🔧 HELPERS
# ==================================================
def extract_filename(text):

    import re

    match = re.search(r'([\w\-]+\.txt)', text)

    if match:
        return match.group(1)

    return "sample.txt"