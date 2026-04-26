# 🤖 Astra — Agentic AI System

## 🎯 Objective

Astra is an agentic AI platform that can understand user intent, generate structured outputs, use tools, retrieve knowledge, and execute real-world tasks via an MCP-style architecture.

---

## 🧠 Architecture

User → LLM → Agent → Tools → Memory → RAG → Response

---

## 🚀 Current Capabilities

* Structured response generation (JSON)
* Reliable LLM interaction with retry & parsing
* Study Assistant (Q&A + summary)

---

## 🔜 Planned Features

* Log Analyzer (Developer Assistant)
* File Analysis Agent
* RAG-based Document QA
* Tool-using Agent (multi-step reasoning)
* MCP-based API integration
* WhatsApp interface (via Twilio)

---

## 🛠 Tech Stack

* Python
* LangChain
* Ollama (Local LLM)
* FastAPI (planned)

---

## 📂 Project Structure

* `core/` → reusable LLM + parsing logic
* `apps/` → user-facing applications
* `experiments/` → step-by-step evolution
* `docs/` → architecture & design

---

## 🎯 End Goal

A production-ready AI assistant capable of:

* reasoning
* tool usage
* knowledge retrieval
* real-world task execution
