from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="gemma:2b")

response = llm.invoke("Tell me what is llm in 2 sentences")

print(response)