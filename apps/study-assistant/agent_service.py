import re
import json
from core.llm import get_llm
from core.tools.calculator import calculator
from core.tools.summarizer import summarizer
from core.tools.file_reader import file_reader
from core.tools.file_analyzer import file_analyzer
from agent_prompt import build_agent_prompt
from core.memory.simple_memory import SimpleMemory

# 🔥 RAG imports
from core.rag.rag_pipeline import index_text, retrieve

llm = get_llm()
memory = SimpleMemory()

TOOLS = {
    "calculator": calculator,
    "summarizer": summarizer,
    "file_reader": file_reader,
    "file_analyzer": file_analyzer
}


def parse_agent_output(text):
    actions = re.findall(r"Action:\s*(.*)", text)
    inputs = re.findall(r"Input:\s*(.*)", text)

    action = actions[0].strip() if actions else None
    action_input = inputs[0].strip() if inputs else None

    return action, action_input


def extract_filename(text):
    match = re.search(r'([\w\-]+\.txt)', text)
    return match.group(1) if match else None


def run_agent(question, max_steps=5):
    scratchpad = ""
    previous_actions = []
    last_result = None

    q = question.lower()

    # 🔥 MEMORY SHORTCUTS
    if any(k in q for k in ["key point", "points", "highlights"]):
        for item in reversed(memory.history):
            if isinstance(item["content"], dict):
                points = item["content"].get("key_points")
                if points:
                    return points

    if "summary" in q:
        for item in reversed(memory.history):
            if isinstance(item["content"], dict):
                summary = item["content"].get("summary")
                if summary:
                    return summary

    # 🔥 RAG RETRIEVAL (before LLM)
    retrieved_chunks = retrieve(question)
    if retrieved_chunks:
        print("📚 Retrieved context:", retrieved_chunks)

        scratchpad += f"""
Relevant context:
{retrieved_chunks}
"""

    for step in range(max_steps):
        print("\n" + "=" * 50)
        print(f"STEP {step + 1}")

        memory_context = memory.get_context()
        prompt = build_agent_prompt(question, scratchpad, memory_context)

        response = llm.invoke(prompt).strip()

        print("\nLLM RESPONSE:\n", response)

        if "Step 2" in response or "Step 3" in response:
            print("⚠️ LLM tried to plan ahead. Forcing first step only.")

        action, action_input = parse_agent_output(response)

        print("\nPARSED ACTION:", action)
        print("PARSED INPUT:", action_input)

        if not action:
            return "Failed to parse action"

        # 🧹 CLEAN + NORMALIZE
        action = action.split("(")[0].strip().lower()

        # 🔀 MULTI-ACTION HANDLING
        if "," in action:
            print("⚠️ Multiple actions detected, taking first one")
            action = action.split(",")[0].strip()

        if "|" in action:
            print("⚠️ Multiple actions detected, taking first one")
            action = action.split("|")[0].strip()

        VALID_ACTIONS = ["calculator", "summarizer", "file_reader", "file_analyzer", "final"]

        # 🎯 INTENT-AWARE FALLBACK
        if action not in VALID_ACTIONS:
            print("⚠️ Invalid action detected")

            file_name = extract_filename(question)

            if file_name:
                print("🔁 File detected → using file_reader")
                action = "file_reader"
                action_input = file_name
            else:
                return "Please provide a file name like sample.txt"

        # 🔥 FORCE CORRECT TOOL FLOW
        if action == "file_analyzer" and ".txt" in str(action_input):
            print("⚠️ Analyzer called with filename → switching to file_reader first")
            action = "file_reader"

        # ✅ FINAL
        if action and action.lower() == "final":
            print("\n✅ FINAL ANSWER REACHED")

            try:
                parsed = json.loads(action_input)

                memory.add("user", question)

                if "summary" in parsed and "key_points" in parsed:
                    memory.add_structured(parsed)
                else:
                    memory.add("assistant", action_input)

                return parsed

            except:
                memory.add("user", question)
                memory.add("assistant", action_input)
                return action_input

        # 🔁 PREVENT REPEAT FILE READ
        if action == "file_reader" and "file_reader" in previous_actions:
            print("⚠️ Preventing repeated file read → switching to analyzer")

            action = "file_analyzer"

            if isinstance(last_result, dict):
                action_input = last_result.get("content", "")

        # 🔁 LOOP DETECTION
        if action in previous_actions:
            return f"Loop detected: '{action}' repeated"

        previous_actions.append(action)

        if action not in TOOLS:
            return f"Unknown action: {action}"

        # 🔧 EXECUTE TOOL
        try:
            result = TOOLS[action](action_input)
            last_result = result
        except Exception as e:
            return f"Tool failed: {str(e)}"

        print("\nTOOL RESULT:", result)

        # 🔥 RAG INDEXING AFTER FILE READ
        if action == "file_reader":
            content = result.get("content", "")
            if content:
                print("📥 Indexing content into vector DB")
                index_text(content)

        # 🧠 SCRATCHPAD UPDATE
        scratchpad += f"""
You have already executed:
Action: {action}
Input: {action_input}

Observation:
{result}

IMPORTANT:
- DO NOT repeat this action again
- Use this observation to decide next step
"""

        # 🔥 SMART EXIT
        if action in ["file_analyzer", "summarizer"]:
            return result

    return "Max steps reached"