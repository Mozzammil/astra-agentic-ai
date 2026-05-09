from core.llm import get_llm
from core.parser.json_parser import parse_json_safe
from core.retry.retry_llm import retry_llm_call

llm = get_llm()

def file_analyzer(input_data):
    """
    Can accept:
    - raw text (string)
    - structured data (dict from previous tools)
    """

    try:
        # 🔥 Handle structured input (from summarizer or other tools)
        if isinstance(input_data, dict):
            text = str(input_data.get("content", ""))
        else:
            text = str(input_data)

        # 🔥 Basic analysis logic (can be improved later with LLM)
        lines = text.split(".")
        key_points = [line.strip() for line in lines if line.strip()][:5]

        summary = text[:150] + "..." if len(text) > 150 else text

        insights = [
            "Content is structured text",
            f"Approx length: {len(text)} characters"
        ]

        return {
            "type": "analysis",
            "content": {
                "summary": summary,
                "key_points": key_points,
                "insights": insights
            },
            "metadata": {
                "length": len(text)
            }
        }

    except Exception as e:
        return {
            "error": str(e)
        }