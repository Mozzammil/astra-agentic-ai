# 🤖 Astra — Agentic AI System

## 📄 Requirements & Architecture Overview

---

## 🎯 Objective

Astra is an **agentic AI system** that can:

* Understand user intent
* Make decisions
* Use tools/APIs
* Retrieve knowledge (RAG)
* Maintain context (memory)
* Return structured, reliable responses

---

## 🧠 Core Idea

Astra follows this simple flow:

```
User → Brain → Decision → Action → Answer
```

Where:

* **Brain** = LLM
* **Decision** = Agent
* **Action** = Tools / APIs
* **Knowledge** = RAG
* **Memory** = Context

---

## 🏗️ High-Level Architecture

```
                ┌──────────────────────┐
                │        User          │
                │ (CLI / WhatsApp/UI) │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Astra Agent        │
                │ (Decision Maker)     │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   LLM (Brain)        │
                │  gemma:2b (Ollama)   │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │  Decision Layer      │
                │ What should I do?    │
                └───────┬─────┬────────┘
                        ↓     ↓
         ┌──────────────┘     └──────────────┐
         ↓                                   ↓
┌───────────────────┐             ┌───────────────────┐
│  Knowledge (RAG)  │             │  Tools / APIs     │
│  Docs, FAQs       │             │  (MCP Layer)      │
└─────────┬─────────┘             └─────────┬─────────┘
          ↓                                 ↓
      Retrieved Data                  Tool Results
                └──────────┬──────────┘
                           ↓
                ┌──────────────────────┐
                │  Memory Layer        │
                │  (Context)           │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │ Structured Output    │
                │ (JSON Response)      │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │     Final Answer     │
                └──────────────────────┘
```

---

## 🧩 System Components

### 1️⃣ User Layer

* CLI (current)
* WhatsApp (future)
* Web UI (optional)

---

### 2️⃣ Astra Agent (Orchestrator)

* Understands user intent
* Decides next step:

  * Answer directly
  * Use tool
  * Retrieve knowledge
  * Use memory

---

### 3️⃣ LLM Layer (Brain)

* Runs locally via Ollama (`gemma:2b`)
* Handles reasoning and response generation

---

### 4️⃣ Decision Layer

Determines:

```
- Should I answer directly?
- Should I call a tool?
- Should I retrieve documents?
- Should I use memory?
```

---

### 5️⃣ Tools / APIs (MCP Layer)

Examples:

* Calculator
* File reader
* Order API
* Log analyzer

Enables real-world actions.

---

### 6️⃣ RAG (Knowledge Layer)

* Stores documents (FAQs, logs, policies)
* Retrieves relevant context
* Enables grounded answers

---

### 7️⃣ Memory Layer

* Maintains conversation context
* Supports follow-up queries

Example:

```
User: What is Java?
User: Give more details
```

---

### 8️⃣ Structured Output Layer

All responses are converted to JSON:

```json
{
  "answer": "...",
  "summary": "...",
  "action": "..."
}
```

Ensures consistency and reliability.

---

## 🔁 End-to-End Flow Example

### Input

```
"Summarize this log file"
```

### Flow

```
User → Agent
      → decides: use file tool
      → tool reads file
      → LLM summarizes
      → JSON output
      → return to user
```

---

## 🧠 Code Mapping

| Layer  | Code             |
| ------ | ---------------- |
| UI     | `main.py`        |
| Agent  | `service.py`     |
| Prompt | `prompts.py`     |
| LLM    | `core/llm.py`    |
| Retry  | `core/retry.py`  |
| Parser | `core/parser.py` |

---

## 🚀 Feature Roadmap

### ✅ Phase 1 — Foundation

* LLM setup
* Python integration
* Prompt control
* JSON output
* Retry + parsing
* Study Assistant

---

### 🔧 Phase 2 — Agent + Tools

* Tool usage
* Multi-step reasoning

---

### 📊 Phase 3 — Memory + RAG

* Context awareness
* Document-based Q&A

---

### 🔗 Phase 4 — MCP Architecture

* External APIs
* Decoupled system

---

### 🚀 Phase 5 — Applications

* Developer Assistant
* Customer Support Agent (WhatsApp)

---

## 🎯 Success Criteria

Astra should be able to:

* Understand user queries
* Generate structured responses
* Use tools when needed
* Retrieve knowledge via RAG
* Maintain context
* Execute real-world actions

---

## 🔥 Final Definition

> Astra is an agentic AI system where an agent uses an LLM to reason, tools to act, and knowledge to answer—while producing structured and reliable outputs.

---
