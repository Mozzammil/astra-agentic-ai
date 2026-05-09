from core.llm import get_llm
from core.tools.calculator import calculator
from core.tools.summarizer import summarizer
from agent_prompt import build_agent_prompt

llm = get_llm()

TOOLS = {
    "calculator": calculator,
    "summarizer": summarizer
}

def parse_agent_output(text):
    lines = text.strip().split("\n")

    action = None
    action_input = None

    for line in lines:
        if line.startswith("Action:"):
            action = line.replace("Action:", "").strip()
        elif line.startswith("Input:"):
            action_input = line.replace("Input:", "").strip()

    return action, action_input


def run_agent(question, max_steps=5):
    scratchpad = ""

    for step in range(max_steps):
        prompt = build_agent_prompt(question, scratchpad)

        response = llm.invoke(prompt)
        print(f"\nSTEP {step+1} RESPONSE:\n{response}")

        action, action_input = parse_agent_output(response)

        if action == "final":
            return action_input

        if action in TOOLS:
            result = TOOLS[action](action_input)

            observation = f"Observation: {result}"

            scratchpad += f"\n{response}\n{observation}\n"
        else:
            return "Invalid action"

    return "Max steps reached"