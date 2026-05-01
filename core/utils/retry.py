def retry_llm_call(llm, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            if response:
                yield response
        except Exception as e:
            print(f"⚠️ Retry {attempt+1} failed:", e)

    yield None