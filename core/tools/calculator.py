def calculator(expression: str):
    """
    Simple calculator tool
    """
    try:
        result = eval(expression)
        return {
            "expression": expression,
            "result": result
        }
    except Exception:
        return {
            "error": "Invalid expression"
        }