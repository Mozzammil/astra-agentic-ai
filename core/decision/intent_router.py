def route_question(question):
    q = question.lower()

    # 🔥 FILE / TOOL intent
    if ".txt" in q or "file" in q:
        return "tool"

    # 🔥 MEMORY intent
    if any(k in q for k in ["key point", "summary", "previous", "earlier"]):
        return "memory"

    # 🔥 RAG intent (knowledge questions)
    if any(k in q for k in ["what is", "explain", "define"]):
        return "rag"

    return "general"