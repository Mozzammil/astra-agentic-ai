import os

from dotenv import load_dotenv

load_dotenv()

# ==================================================
# 🔥 PROVIDER CONFIG
# ==================================================
LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
).lower()


# ==================================================
# 🚀 MAIN FACTORY
# ==================================================
def get_llm():

    print(f"\n🧠 Using Provider: {LLM_PROVIDER}")

    # ==================================================
    # 🔥 OLLAMA
    # ==================================================
    if LLM_PROVIDER == "ollama":

        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3"
            ),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            ),
            temperature=0
        )

    # ==================================================
    # 🔥 OPENAI
    # ==================================================
    elif LLM_PROVIDER == "openai":

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=os.getenv(
                "OPENAI_API_KEY"
            ),
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4o-mini"
            ),
            temperature=0
        )

    # ==================================================
    # 🔥 GEMINI
    # ==================================================
    elif LLM_PROVIDER == "gemini":

        from langchain_google_genai import (
            ChatGoogleGenerativeAI
        )

        return ChatGoogleGenerativeAI(
            google_api_key=os.getenv(
                "GEMINI_API_KEY"
            ),
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-1.5-flash"
            ),
            temperature=0
        )

    # ==================================================
    # 🚫 INVALID PROVIDER
    # ==================================================
    raise ValueError(
        f"Unsupported provider: {LLM_PROVIDER}"
    )

