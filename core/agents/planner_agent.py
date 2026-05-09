from core.agents.planner import create_plan


class PlannerAgent:

    def __init__(self):
        self.max_steps = 5

    # ==================================================
    # 🧠 MAIN PLANNER ENTRY
    # ==================================================
    def run(
        self,
        question,
        memory_context="",
        rag_context=""
    ):
        print("\n🧠 Planner Agent Running")

        try:
            # ==================================================
            # 🔥 CREATE PLAN
            # ==================================================
            plan = create_plan(
                question=question,
                memory_context=memory_context,
                rag_context=rag_context
            )

            print("\n📋 RAW PLAN:")
            print(plan)

            # ==================================================
            # 🚫 EMPTY PLAN
            # ==================================================
            if not plan:
                print("⚠️ Empty plan generated")

                return self.fallback_plan(question)

            # ==================================================
            # 🔥 VALIDATE PLAN
            # ==================================================
            validated_plan = self.validate_plan(plan)

            print("\n✅ VALIDATED PLAN:")
            print(validated_plan)

            return validated_plan

        except Exception as e:
            print("❌ Planner Agent Failed:", str(e))

            return self.fallback_plan(question)

    # ==================================================
    # 🔥 PLAN VALIDATION
    # ==================================================
    def validate_plan(self, plan):

        VALID_ACTIONS = [
            "file_reader",
            "summarizer",
            "file_analyzer",
            "calculator"
        ]

        validated = []

        for step in plan:

            # 🔥 Ignore bad steps
            if not isinstance(step, dict):
                continue

            action = step.get("action")
            action_input = step.get("input")
            reason = step.get("reason", "")

            # 🚫 Missing action
            if not action:
                continue

            action = action.strip()

            # 🚫 Invalid action
            if action not in VALID_ACTIONS:
                print(f"⚠️ Invalid action removed: {action}")
                continue

            # 🔥 Auto-fix missing input
            if action_input is None:
                action_input = ""

            validated.append({
                "action": action,
                "input": action_input,
                "reason": reason
            })

        # 🚫 Too many steps
        if len(validated) > self.max_steps:
            validated = validated[:self.max_steps]

        return validated

    # ==================================================
    # 🛡️ FALLBACK PLAN
    # ==================================================
    def fallback_plan(self, question):

        q = question.lower()

        print("🛡️ Using fallback planner")

        # ==================================================
        # 🔥 FILE ANALYSIS
        # ==================================================
        if "analyze" in q and ".txt" in q:

            filename = self.extract_filename(question)

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

            filename = self.extract_filename(question)

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

            filename = self.extract_filename(question)

            return [
                {
                    "action": "file_reader",
                    "input": filename,
                    "reason": "Read file content"
                }
            ]

        # ==================================================
        # 🔥 NO PLAN
        # ==================================================
        return []

    # ==================================================
    # 🔧 HELPERS
    # ==================================================
    def extract_filename(self, text):

        import re

        match = re.search(r'([\w\-]+\.txt)', text)

        if match:
            return match.group(1)

        return "sample.txt"