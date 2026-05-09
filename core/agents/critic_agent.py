import json

from core.llm import get_llm

llm = get_llm()


class CriticAgent:

    def __init__(self):
        self.confidence_threshold = 70

    # ==================================================
    # 🧠 MAIN REFLECTION ENTRY
    # ==================================================
    def reflect(self, question, answer):

        print("\n🧠 Critic Agent Running")

        # ==================================================
        # 🚫 EMPTY ANSWER
        # ==================================================
        if not answer:
            return "No answer generated."

        # ==================================================
        # 📊 CONFIDENCE CHECK
        # ==================================================
        confidence = self.evaluate_confidence(
            question,
            answer
        )

        print("\n📊 CONFIDENCE RESULT:")
        print(confidence)

        score = confidence.get("score", 50)

        # ==================================================
        # 🔁 LOW CONFIDENCE → RETRY
        # ==================================================
        if (
            score < self.confidence_threshold
            or confidence.get("retry_needed")
        ):

            print("\n🔁 Low confidence detected")

            retried_answer = self.retry_answer(
                question,
                answer
            )

            # 🔥 REFLECT AGAIN
            improved = self.reflect_and_improve(
                question,
                retried_answer
            )

            return improved

        # ==================================================
        # 🔥 NORMAL REFLECTION
        # ==================================================
        improved = self.reflect_and_improve(
            question,
            answer
        )

        return improved

    # ==================================================
    # 📊 CONFIDENCE EVALUATION
    # ==================================================
    def evaluate_confidence(
        self,
        question,
        answer
    ):

        prompt = f"""
You are an AI evaluator.

Question:
{question}

Answer:
{answer}

Evaluate:
1. correctness
2. completeness
3. clarity
4. confidence

Return ONLY valid JSON:

{{
  "score": 0-100,
  "reason": "short explanation",
  "retry_needed": true/false
}}
"""

        try:

            response = llm.invoke(prompt)

            print("\n🧠 CONFIDENCE RAW:")
            print(response)

            data = self.safe_json_parse(response)

            if not data:
                return self.default_confidence()

            return {
                "score": data.get("score", 50),
                "reason": data.get(
                    "reason",
                    "No reason"
                ),
                "retry_needed": data.get(
                    "retry_needed",
                    False
                )
            }

        except Exception as e:

            print("⚠️ Confidence evaluation failed:")
            print(str(e))

            return self.default_confidence()

    # ==================================================
    # 🔁 RETRY ANSWER
    # ==================================================
    def retry_answer(
        self,
        question,
        previous_answer
    ):

        prompt = f"""
The previous answer may be weak.

Question:
{question}

Previous Answer:
{previous_answer}

Generate a BETTER answer:
- more accurate
- more complete
- better reasoning
"""

        try:

            improved = llm.invoke(prompt)

            print("\n🔁 RETRY RESPONSE:")
            print(improved)

            return improved

        except Exception as e:

            print("⚠️ Retry failed:")
            print(str(e))

            return previous_answer

    # ==================================================
    # 🧠 REFLECTION + IMPROVEMENT
    # ==================================================
    def reflect_and_improve(
        self,
        question,
        result
    ):

        prompt = f"""
You are an AI critic.

Question:
{question}

Answer:
{result}

Check:
- correctness
- completeness
- clarity
- missing details
- reasoning quality

Return ONLY valid JSON:

{{
  "is_correct": true/false,
  "issues": ["list of issues"],
  "improved_answer": "better version"
}}
"""

        try:

            response = llm.invoke(prompt)

            print("\n🧠 REFLECTION RAW:")
            print(response)

            data = self.safe_json_parse(response)

            if not data:
                return result

            # ==================================================
            # ✅ ANSWER GOOD
            # ==================================================
            if data.get("is_correct", True):

                improved = data.get(
                    "improved_answer"
                )

                if improved:
                    return improved

                return result

            # ==================================================
            # ⚠️ IMPROVE ANSWER
            # ==================================================
            print("\n⚠️ Issues Found:")
            print(data.get("issues"))

            improved = data.get(
                "improved_answer"
            )

            if improved:
                return improved

            return result

        except Exception as e:

            print("⚠️ Reflection failed:")
            print(str(e))

            return result

    # ==================================================
    # 🔧 SAFE JSON PARSE
    # ==================================================
    def safe_json_parse(self, text):

        try:

            # 🔥 extract JSON block
            start = text.find("{")
            end = text.rfind("}") + 1

            if start == -1 or end == -1:
                return None

            cleaned = text[start:end]

            return json.loads(cleaned)

        except Exception as e:

            print("⚠️ JSON parse failed:")
            print(str(e))

            return None

    # ==================================================
    # 🔧 DEFAULT CONFIDENCE
    # ==================================================
    def default_confidence(self):

        return {
            "score": 50,
            "reason": "Confidence evaluation failed",
            "retry_needed": False
        }