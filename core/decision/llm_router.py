from core.llm import get_llm
import json

llm = get_llm()


ROUTER_PROMPT = """
You are an AI decision engine.

Your job is to decide how to handle a user query.

Choose ONE action from:
- memory → if user is asking about previous result (summary, key points)
- rag → if user is asking knowledge questions from documents
- tool → if user wants to analyze file or calculate something
- answer → if general question

Respond ONLY in JSON:

{{
  "route": "memory | rag | tool | answer",
  "reason": "short explanation"
}}

User Question:
{question}
"""


def route_with_llm(question):
    prompt = ROUTER_PROMPT.format(question=question)

    response = llm.invoke(prompt)

    try:
        data = json.loads(response)
        return data.get("route", "answer")
    except:
        return "answer"