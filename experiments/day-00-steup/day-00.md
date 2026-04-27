# Day 00 — Setup Local LLM + Python Integration

## 🎯 Objective

Set up a local LLM, verify it works via CLI, and integrate it with Python.
This establishes the base for Astra’s agentic AI system.

---

## ⚙️ Step 1 — Install Ollama

Install:

* Ollama (local LLM runtime)

Verify installation:

```bash
ollama --version
```

---

## ⚙️ Step 2 — Pull & Run Lightweight Model

We used a lightweight model for faster iteration:

```bash
ollama pull gemma:2b
ollama run gemma:2b
```

This:

* Downloads the model
* Starts an interactive session

---

## 🧪 Step 3 — Test LLM via CLI

Test basic prompts:

```text
What is Java?
Explain microservices in 2 lines
Give 3 backend interview questions
```

### Observations:

* Responses are fast (compared to larger models)
* Output varies slightly (non-deterministic)
* Instruction following is decent but not perfect

---


## 🧠 Key Learnings

* LLM can run locally using Ollama
