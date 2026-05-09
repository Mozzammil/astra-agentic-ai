from core.llm import get_llm
from core.memory.simple_memory import SimpleMemory

# 🔥 Agents
from core.agents.router_agent import RouterAgent
from core.agents.planner_agent import PlannerAgent
from core.agents.executor_agent import ExecutorAgent
from core.agents.critic_agent import CriticAgent

# 🔥 RAG
from core.rag.rag_pipeline import retrieve

llm = get_llm()
memory = SimpleMemory()

# ==================================================
# 🚀 AGENT INITIALIZATION
# ==================================================
router_agent = RouterAgent()
planner_agent = PlannerAgent()
executor_agent = ExecutorAgent()
critic_agent = CriticAgent()


# ==================================================
# 🧠 MAIN ORCHESTRATOR
# ==================================================
def run_agent(question):
    print("\n" + "=" * 50)
    print("Ask:", question)

    # ==================================================
    # 🧭 ROUTER AGENT
    # ==================================================
    intent = router_agent.run(question)

    if not intent:
        intent = "answer"

    intent = intent.strip().lower()

    print("\n🧠 FINAL INTENT:", intent)

    VALID_INTENTS = ["memory", "rag", "tool", "answer"]

    if intent not in VALID_INTENTS:
        print("⚠️ Invalid intent → fallback to answer")
        intent = "answer"

    # 🔥 HARD OVERRIDE FOR FILES
    if ".txt" in question.lower() or "file" in question.lower():
        print("🛠️ File query detected → forcing TOOL intent")
        intent = "tool"

    # ==================================================
    # 🧠 MEMORY FLOW
    # ==================================================
    if intent == "memory":

        print("\n🧠 Memory Agent Logic")

        for item in reversed(memory.history):

            if isinstance(item["content"], dict):

                if "key point" in question.lower():
                    result = item["content"].get("key_points")

                    final_answer = critic_agent.reflect(
                        question,
                        result
                    )

                    return final_answer

                if "summary" in question.lower():
                    result = item["content"].get("summary")

                    final_answer = critic_agent.reflect(
                        question,
                        result
                    )

                    return final_answer

        return "No relevant memory found."

    # ==================================================
    # 🔍 RAG FLOW
    # ==================================================
    rag_context = ""

    if intent == "rag":

        print("\n🔍 Retrieving RAG context")

        rag_context = retrieve(question)

        print("📚 RAG CONTEXT:", rag_context)

    # ==================================================
    # 🧠 PLANNER AGENT
    # ==================================================
    memory_context = memory.get_context()

    print("\n🧠 Planner Agent Starting")

    plan = planner_agent.run(
        question,
        memory_context=memory_context,
        rag_context=rag_context
    )

    print("\n📋 GENERATED PLAN:")
    print(plan)

    # ==================================================
    # 🚫 EMPTY PLAN FALLBACK
    # ==================================================
    if not plan:

        print("⚠️ Empty plan → fallback to direct LLM")

        raw_response = llm.invoke(question)

        final_answer = critic_agent.reflect(
            question,
            raw_response
        )

        memory.add("user", question)
        memory.add("assistant", final_answer)

        return final_answer

    # ==================================================
    # ⚙️ EXECUTOR AGENT
    # ==================================================
    print("\n⚙️ Executor Agent Starting")

    result = executor_agent.run(plan)

    print("\n🔍 EXECUTION RESULT:")
    print(result)

    # ==================================================
    # 🚫 EXECUTION FAILURE FALLBACK
    # ==================================================
    if isinstance(result, str) and "error" in result.lower():

        print("⚠️ Execution failed → fallback to LLM")

        raw_response = llm.invoke(question)

        final_answer = critic_agent.reflect(
            question,
            raw_response
        )

        memory.add("user", question)
        memory.add("assistant", final_answer)

        return final_answer

    # ==================================================
    # 🧠 CRITIC AGENT (SELF-REFLECTION)
    # ==================================================
    print("\n🧠 Critic Agent Starting")

    final_answer = critic_agent.reflect(
        question,
        result
    )

    print("\n✨ FINAL IMPROVED ANSWER:")
    print(final_answer)

    # ==================================================
    # 💾 MEMORY STORAGE
    # ==================================================
    memory.add("user", question)

    if isinstance(final_answer, dict):
        memory.add_structured(final_answer)
    else:
        memory.add("assistant", str(final_answer))

    return final_answer