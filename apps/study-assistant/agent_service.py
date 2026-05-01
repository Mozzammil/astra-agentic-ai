import re
import json
from core.llm import get_llm
from core.tools.calculator import calculator
from core.tools.summarizer import summarizer
from core.tools.file_reader import file_reader
from core.tools.file_analyzer import file_analyzer
from agent_prompt import build_agent_prompt
from core.memory.simple_memory import SimpleMemory

# 🔥 RAG
from core.rag.rag_pipeline import index_text, retrieve

# 🔥 Decision Engine
from core.decision.llm_router import route_with_llm

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

    # 🧠 INTENT DETECTION
    intent = route_with_llm(question)
    intent = intent.strip().lower()
    print("🧠 Detected intent:", intent)

    # ✅ VALIDATION GUARD (ADD HERE)
    VALID_INTENTS = ["memory", "rag", "tool", "answer"]

    if intent not in VALID_INTENTS:
        print("⚠️ Invalid intent from LLM → fallback to answer")
        intent = "answer"

    # ==================================================
    # 🔥 MEMORY INTENT (FAST PATH - NO LLM)
    # ==================================================
    if intent == "memory":
        for item in reversed(memory.history):
            if isinstance(item["content"], dict):

                if "key point" in question.lower():
                    points = item["content"].get("key_points")
                    if points:
                        return points

                if "summary" in question.lower():
                    summary = item["content"].get("summary")
                    if summary:
                        return summary

        return "No relevant memory found."

    # ==================================================
    # 🔥 RAG CONTEXT INJECTION (BEFORE LLM)
    # ==================================================
    if intent == "rag":
        retrieved_chunks = retrieve(question)

        if retrieved_chunks:
            print("📚 Using RAG context:", retrieved_chunks)

            scratchpad += f"""
Relevant context:
{retrieved_chunks}

IMPORTANT:
- Answer ONLY using this context
"""

    # ==================================================
    # 🔁 MAIN AGENT LOOP
    # ==================================================
    for step in range(max_steps):
        print("\n" + "=" * 50)
        print(f"STEP {step + 1}")

        memory_context = memory.get_context()
        prompt = build_agent_prompt(question, scratchpad, memory_context)

        response = llm.invoke(prompt).strip()

        print("\nLLM RESPONSE:\n", response)

        # ⚠️ Multi-step hallucination guard
        if "Step 2" in response or "Step 3" in response:
            print("⚠️ LLM tried to plan ahead. Forcing first step only.")

        action, action_input = parse_agent_output(response)

        print("\nPARSED ACTION:", action)
        print("PARSED INPUT:", action_input)

        if not action:
            return "Failed to parse action"

        # 🧹 CLEAN ACTION
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

            if intent == "tool" and file_name:
                print("🔁 Tool intent → forcing file_reader")
                action = "file_reader"
                action_input = file_name
            else:
                return "I couldn't understand the action. Please rephrase."

        # 🔥 FORCE CORRECT FLOW
        if action == "file_analyzer" and ".txt" in str(action_input):
            print("⚠️ Analyzer called with filename → switching to file_reader")
            action = "file_reader"

        # ==================================================
        # ✅ FINAL RESPONSE
        # ==================================================
        if action == "final":
            print("\n✅ FINAL ANSWER REACHED")

            try:
                parsed = json.loads(action_input)

                memory.add("user", question)

                # store structured memory only if valid
                if isinstance(parsed, dict) and "summary" in parsed:
                    memory.add_structured(parsed)
                else:
                    memory.add("assistant", action_input)

                return parsed

            except:
                memory.add("user", question)
                memory.add("assistant", action_input)
                return action_input

        # ==================================================
        # 🔁 LOOP & TOOL CONTROL
        # ==================================================
        if action == "file_reader" and "file_reader" in previous_actions:
            print("⚠️ Preventing repeated file read → switching to analyzer")

            action = "file_analyzer"

            if isinstance(last_result, dict):
                action_input = last_result.get("content", "")

        if action in previous_actions:
            return f"Loop detected: '{action}' repeated"

        previous_actions.append(action)

        if action not in TOOLS:
            return f"Unknown action: {action}"

        # ==================================================
        # 🔧 EXECUTE TOOL
        # ==================================================
        try:
            result = TOOLS[action](action_input)
            last_result = result
        except Exception as e:
            return f"Tool failed: {str(e)}"

        print("\nTOOL RESULT:", result)

        # ==================================================
        # 🔥 RAG INDEXING (AFTER FILE READ)
        # ==================================================
        if action == "file_reader":
            content = result.get("content", "")
            if content:
                print("📥 Indexing content into vector DB")
                index_text(content)

        # ==================================================
        # 🧠 SCRATCHPAD UPDATE
        # ==================================================
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

        # ==================================================
        # 🔥 SMART EXIT
        # ==================================================
        if action in ["file_analyzer", "summarizer"]:
            return result

    return "Max steps reached"