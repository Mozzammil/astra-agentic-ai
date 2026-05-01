def summarizer(text: str):
    """
    Simple summarizer tool (mock for now)
    """
    return {
        "original_length": len(text),
        "summary": text[:100] + "..." if len(text) > 100 else text
    }