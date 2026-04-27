# 🚀 Astra — Phase 1 Requirements

## 📄 Foundation Layer (LLM Reliability & Structured Output)

---

## 🎯 Objective

Build a **reliable LLM interaction layer** that:

* Accepts user input
* Controls LLM output
* Returns structured JSON responses
* Handles inconsistencies and failures

---

## 🧠 Scope of Phase 1

Phase 1 focuses on **core LLM capabilities**, not full agent behavior.

> No tools, no RAG, no MCP yet — only a strong foundation.

---

## 🧩 Functional Requirements

### 1. LLM Setup

* System must run a local LLM using Ollama
* Must support lightweight model (`gemma:2b`)
* Must allow CLI-based interaction

---

### 2. Python Integration

* LLM must be callable from Python
* Should behave like a function:

```text
input → response
```

---

### 3. Prompt Control

* System must enforce structured output
* Responses must follow predefined JSON schema

Example:

```json
{
  "question": "string",
  "answer": "string",
  "summary": "string"
}
```

---

### 4. Output Parsing

* System must extract JSON from LLM response
* Must handle extra text or malformed output

---

### 5. Retry Mechanism

* System must retry LLM call if parsing fails
* Maximum retry attempts should be configurable (default: 3)

---

### 6. Error Handling

* System must not crash on invalid output
* Should return fallback response:

```json
{
  "error": "final_failure"
}
```

---

### 7. First Application (Study Assistant)

* System must include a basic app that:

  * Accepts a question
  * Returns answer + summary in JSON

---

## ⚙️ Non-Functional Requirements

* Fast response time (optimized for local models)
* Modular code structure
* Separation of concerns:

  * LLM layer
  * Prompt layer
  * Parsing layer
  * Retry logic
* Maintainable and extensible architecture

---

## 🧠 Constraints

* Local LLM has limited reasoning ability
* Output is non-deterministic
* JSON format may break without control mechanisms

---

## 📦 Deliverables

* Working LLM integration
* Structured prompt system
* JSON parsing module
* Retry logic module
* Study Assistant application
* Code pushed to GitHub

---

## ✅ Success Criteria

Phase 1 is complete when:

* LLM responds via Python
* Output is mostly valid JSON
* System handles parsing failures gracefully
* Study Assistant works end-to-end
* No crashes in repeated runs

---

## 🔥 Outcome

After Phase 1, Astra becomes:

> A reliable system that converts unstructured LLM output into structured, usable data.

---

## 🚀 Next Phase

Phase 2 will introduce:

* Tool usage
* Agent decision-making
* Multi-step reasoning

---
