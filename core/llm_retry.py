def retry_llm_call(llm, prompt, attempts=3):
    for _ in range(attempts):
        yield llm.invoke(prompt)