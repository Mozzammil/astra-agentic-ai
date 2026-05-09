def calculator(expr):
    result = eval(expr)

    return {
        "type": "math",
        "content": result,
        "metadata": {"expression": expr}
    }