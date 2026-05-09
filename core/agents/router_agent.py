from core.decision.llm_router import route_with_llm


class RouterAgent:

    def __init__(self):
        self.valid_intents = [
            "memory",
            "rag",
            "tool",
            "answer"
        ]

    # ==================================================
    # 🧭 MAIN ROUTER
    # ==================================================
    def run(self, question):
        print("\n🧭 Router Agent Running")

        try:
            intent = route_with_llm(question)

            if not intent:
                print("⚠️ Empty intent from LLM")
                return self.rule_based_fallback(question)

            intent = intent.strip().lower()

            print("🧠 Raw Intent:", intent)

            # ==================================================
            # 🔥 VALIDATION
            # ==================================================
            if intent not in self.valid_intents:
                print("⚠️ Invalid intent from LLM")

                return self.rule_based_fallback(question)

            return intent

        except Exception as e:
            print("❌ Router failed:", str(e))

            return self.rule_based_fallback(question)

    # ==================================================
    # 🛡️ RULE-BASED FALLBACK
    # ==================================================
    def rule_based_fallback(self, question):

        q = question.lower()

        print("🛡️ Using fallback routing")

        # 🔥 FILE QUERIES
        if ".txt" in q or "file" in q:
            return "tool"

        # 🔥 MEMORY QUERIES
        if any(word in q for word in [
            "remember",
            "recall",
            "previous",
            "last time",
            "summary",
            "key points"
        ]):
            return "memory"

        # 🔥 TOOL QUERIES
        if any(op in q for op in ["+", "-", "*", "/"]):
            return "tool"

        if any(word in q for word in [
            "calculate",
            "analyze",
            "summarize"
        ]):
            return "tool"

        # 🔥 RAG QUERIES
        if any(word in q for word in [
            "document",
            "knowledge",
            "context"
        ]):
            return "rag"

        # 🔥 DEFAULT
        return "answer"