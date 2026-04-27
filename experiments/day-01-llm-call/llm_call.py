from langchain_ollama import OllamaLLM

# Initialize model
llm = OllamaLLM(
    model="gemma:2b",
    temperature=0.2
)

# Test prompts
print(llm.invoke("Explain Java in 2 lines"))
print("------")
print(llm.invoke("You are a senior backend engineer. Explain microservices"))