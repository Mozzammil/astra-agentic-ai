def summarizer(text):
    summary = text[:100] + "..." if len(text) > 100 else text

    return {
        "type": "text",
        "content": summary,
        "metadata": {"original_length": len(text)}
    }