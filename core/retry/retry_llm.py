def retry_llm_call(llm, prompt, retries=3):
    for attempt in range(retries):
        response = llm.invoke(prompt)

        yield response