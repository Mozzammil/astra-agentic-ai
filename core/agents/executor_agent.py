import os
from difflib import get_close_matches

from core.tools.calculator import calculator
from core.tools.summarizer import summarizer
from core.tools.file_reader import file_reader
from core.tools.file_analyzer import file_analyzer
from core.rag.rag_pipeline import index_text
from core.llm import get_llm

llm = get_llm()

# ==================================================
# 🔧 AVAILABLE TOOLS
# ==================================================
TOOLS = {
    "calculator": calculator,
    "summarizer": summarizer,
    "file_reader": file_reader,
    "file_analyzer": file_analyzer
}


class ExecutorAgent:

    # ==================================================
    # 🚀 MAIN EXECUTION ENTRY
    # ==================================================
    def run(self, plan):

        print("\n⚙️ Executor Agent Running")

        if not plan or not isinstance(plan, list):
            return "Invalid or empty plan"

        context = {}
        results = []

        for step in plan:

            action = step.get("action")
            action_input = step.get("input")
            reason = step.get("reason", "")

            print("\n" + "=" * 50)
            print(f"🧠 Action: {action}")
            print(f"💡 Reason: {reason}")

            # ==================================================
            # 🔥 PLACEHOLDER RESOLUTION
            # ==================================================
            resolved_input = self.resolve_input(
                action_input,
                context
            )

            # 🚫 Missing dependency
            if resolved_input is None:
                return f"Missing dependency for {action}"

            print(f"🚀 Executing: {action}")
            print(f"📥 Input: {resolved_input}")

            # ==================================================
            # 🔥 VALIDATION
            # ==================================================
            if action not in TOOLS:
                return f"Unknown action: {action}"

            # ==================================================
            # 🔥 EXECUTE WITH SELF-HEALING
            # ==================================================
            result = self.execute_tool_with_repair(
                action,
                resolved_input
            )

            print("\n🔍 TOOL RESULT:")
            print(result)

            # ==================================================
            # 🚫 HARD FAILURE CHECK
            # ==================================================
            if (
                not result or
                isinstance(result, dict) and result.get("error")
            ):
                print("❌ Tool execution failed")

                return result

            # ==================================================
            # 🧠 CONTEXT SHARING
            # ==================================================
            self.update_context(
                context,
                action,
                result
            )

            # ==================================================
            # 🔥 AUTO RAG INDEXING
            # ==================================================
            if action == "file_reader":

                content = result.get("content")

                if content:
                    print("📥 Indexing content into RAG")

                    try:
                        index_text(content)
                    except Exception as e:
                        print("⚠️ RAG indexing failed:", str(e))

            results.append(result)

        # ==================================================
        # ✅ FINAL RESULT
        # ==================================================
        if results:
            return results[-1]

        return "No execution result"

    # ==================================================
    # 🔥 CONTEXT UPDATE
    # ==================================================
    def update_context(
        self,
        context,
        action,
        result
    ):

        if not isinstance(result, dict):
            return

        # ==================================================
        # 🔥 FILE CONTENT
        # ==================================================
        if action == "file_reader":

            context["content"] = result.get("content")

        # ==================================================
        # 🔥 SUMMARY
        # ==================================================
        elif action == "summarizer":

            context["summary"] = result.get("summary")

        # ==================================================
        # 🔥 ANALYSIS
        # ==================================================
        elif action == "file_analyzer":

            context["analysis"] = result

        # ==================================================
        # 🔥 MATH
        # ==================================================
        elif action == "calculator":

            context["math_result"] = result

    # ==================================================
    # 🔥 PLACEHOLDER RESOLUTION
    # ==================================================
    def resolve_input(
        self,
        action_input,
        context
    ):

        if not action_input:
            return None

        action_input = str(action_input)

        # ==================================================
        # 🔥 <content>
        # ==================================================
        if "<content>" in action_input:

            value = context.get("content")

            if not value:
                return None

            return value

        # ==================================================
        # 🔥 <summary>
        # ==================================================
        if "<summary>" in action_input:

            value = context.get("summary")

            if not value:
                return None

            return value

        # ==================================================
        # 🔥 <analysis>
        # ==================================================
        if "<analysis>" in action_input:

            value = context.get("analysis")

            if not value:
                return None

            return value

        return action_input

    # ==================================================
    # 🔥 EXECUTE TOOL WITH REPAIR
    # ==================================================
    def execute_tool_with_repair(
        self,
        action,
        action_input
    ):

        try:

            result = TOOLS[action](action_input)

            # 🚫 TOOL-LEVEL ERROR
            if (
                isinstance(result, dict)
                and result.get("error")
            ):
                raise Exception(result["error"])

            return result

        except Exception as e:

            print("\n❌ TOOL FAILED:")
            print(str(e))

            # ==================================================
            # 🔥 AUTO-CORRECTION
            # ==================================================
            corrected_input = self.correct_tool_input(
                action,
                action_input,
                str(e)
            )

            print("\n🛠️ Corrected Input:")
            print(corrected_input)

            print("🔁 Retrying tool")

            try:

                repaired_result = TOOLS[action](
                    corrected_input
                )

                print("✅ Repair successful")

                return repaired_result

            except Exception as retry_error:

                print("❌ Repair failed")

                return {
                    "error": str(retry_error)
                }

    # ==================================================
    # 🔥 INPUT CORRECTION
    # ==================================================
    def correct_tool_input(
        self,
        action,
        bad_input,
        error
    ):

        # ==================================================
        # 🔥 FILE AUTO-CORRECTION
        # ==================================================
        if action == "file_reader":

            corrected = self.find_similar_file(
                str(bad_input)
            )

            print("📂 Similar file detected:")
            print(corrected)

            return corrected

        # ==================================================
        # 🔥 LLM-BASED CORRECTION
        # ==================================================
        prompt = f"""
You are an AI tool correction system.

Tool:
{action}

Bad Input:
{bad_input}

Error:
{error}

Fix the input intelligently.

Return ONLY corrected input.
"""

        try:

            corrected = llm.invoke(prompt).strip()

            return corrected

        except Exception:

            return bad_input

    # ==================================================
    # 🔥 SIMILAR FILE SEARCH
    # ==================================================
    def find_similar_file(
        self,
        filename
    ):

        try:

            data_dir = "data"

            if not os.path.exists(data_dir):
                return filename

            files = os.listdir(data_dir)

            matches = get_close_matches(
                filename,
                files,
                n=1,
                cutoff=0.6
            )

            if matches:
                return matches[0]

        except Exception as e:

            print("⚠️ Similar file search failed:")
            print(str(e))

        return filename