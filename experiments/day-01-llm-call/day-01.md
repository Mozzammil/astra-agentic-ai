# Day 01 — LLM as a Function (Python Integration)

## 🎯 Objective

Integrate the local LLM with Python and treat it as a callable function.

---

## ⚙️ Step 1 — Install Dependencies

```bash
pip install langchain
pip install langchain-ollama
```

---

## 🧩 Step 2 — Call LLM from Python

### File: `day-01-llm-call/llm_call.py`

```python
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
```

---

## ▶️ Step 3 — Run the Script

```bash
python llm_call.py
```

---

## 🧪 Experiments Performed

* Basic prompt
* Role-based prompt

---

## ⚠️ Observations

* Same prompt gives slightly different outputs
* Responses depend heavily on prompt wording
* Output is not structured

---

## 🧠 Key Learnings

* LLM behaves like a function:
  `input → response`
* Output is **non-deterministic**
* Prompt engineering is critical for control

---

## ⚠️ Issues Faced

* Deprecated import warning → fixed using:

```python
from langchain_ollama import OllamaLLM
```

---

## ✅ Outcome

* Successfully invoked LLM from Python
* Verified prompt-based behavior
* Ready for structured output and prompt control

---

## 🚀 Next Step

Move to:

* Prompt engineering
* Structured JSON output
