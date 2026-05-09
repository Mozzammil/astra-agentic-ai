# 📄 Scope Document — Configurable LLM Provider Support

## 🎯 Objective

Add configuration-driven LLM provider support to Astra so the system can dynamically switch between:

* Local LLMs (Ollama)
* Cloud LLMs (OpenAI, Gemini, etc.)

without changing application code.

---

# 🚀 Current Problem

Currently the LLM provider is hardcoded.

Example:

```python id="u7ynk7"
ChatOllama(model="llama3")
```

Problems:

* tightly coupled architecture
* difficult provider switching
* no environment-based configuration
* hard to benchmark models
* difficult production deployment

---

# ✅ Proposed Solution

Introduce a centralized LLM abstraction layer using:

* `.env` configuration
* provider-based factory pattern
* dynamic provider loading

---

# 🧠 Target Architecture

```text id="xjoc90"
Application
     ↓
get_llm()
     ↓
LLM Factory
     ↓
Provider Selection
     ↓
Local / Cloud LLM
```

---

# 🔧 Supported Providers (Phase 1)

| Provider | Type  |
| -------- | ----- |
| Ollama   | Local |
| OpenAI   | Cloud |
| Gemini   | Cloud |

---

# 📁 Files Impacted

| File               | Change                     |
| ------------------ | -------------------------- |
| `.env`             | Add provider configuration |
| `core/llm.py`      | Implement LLM factory      |
| `requirements.txt` | Add provider SDKs          |
| `README.md`        | Add setup documentation    |

---

## 📦 Required Installations

Install required dependencies before running the system.

### Core Environment Support

```bash
pip install python-dotenv
```

### Ollama Provider

```bash
pip install langchain-ollama
```

### OpenAI Provider

```bash
pip install langchain-openai
```

### Gemini Provider

```bash
pip install langchain-google-genai
```

### Recommended Combined Installation

```bash
pip install python-dotenv langchain-ollama langchain-openai langchain-google-genai
```

---


# ⚙️ Environment Variables

## Example

```properties id="d94rwa"
LLM_PROVIDER=ollama

OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash
```

---

# 🧠 Functional Requirements

## ✅ Provider Selection

System must dynamically select provider from configuration.

---

## ✅ Local LLM Support

System must support Ollama-hosted models.

---

## ✅ Cloud LLM Support

System must support cloud APIs.

---

## ✅ Zero Code Change Switching

Switching providers should require only `.env` changes.

---

## ✅ Backward Compatibility

Existing agent architecture should continue working unchanged.

---

# 🔥 Non-Functional Requirements

| Requirement     | Goal                       |
| --------------- | -------------------------- |
| Scalability     | Add new providers easily   |
| Maintainability | Centralized LLM logic      |
| Reliability     | Invalid provider detection |
| Extensibility   | Future provider expansion  |
| Security        | API keys via env vars      |

---

# 🧠 Technical Design

## Factory Pattern

```python id="jlwm9u"
get_llm()
```

returns provider-specific client.

---

## Dynamic Imports

Load provider SDKs only when needed.

---

## Provider Isolation

Each provider encapsulated independently.

---

# 🚀 Future Enhancements (Out of Scope)

These are NOT included in current implementation.

---

## ❌ Multi-LLM Fallback

Example:

```text id="4jlwm7"
OpenAI → fallback to Gemini
```

---

## ❌ Load Balancing

---

## ❌ Automatic Cost Optimization

---

## ❌ Dynamic Model Selection

---

## ❌ Streaming Responses

---

# 🧪 Testing Scope

## Functional Tests

| Test             | Expected          |
| ---------------- | ----------------- |
| Ollama config    | local model works |
| OpenAI config    | cloud model works |
| Gemini config    | cloud model works |
| Invalid provider | proper error      |
| Missing API key  | graceful failure  |

---

# 🔥 Risks

| Risk               | Mitigation            |
| ------------------ | --------------------- |
| Missing SDK        | install validation    |
| Invalid env config | fallback + validation |
| API failures       | future retry support  |
| Model mismatch     | provider validation   |

---

# 📈 Expected Outcome

Astra becomes:

```text id="yjlwm3"
Provider-independent AI platform
```

instead of:

```text id="jlwm5r"
Single-LLM hardcoded system
```

---

# 🏁 Final Deliverable

A configurable AI infrastructure where:

```properties id="jlwm11"
LLM_PROVIDER=ollama
```

or

```properties id="jlwm12"
LLM_PROVIDER=openai
```

changes the entire AI backend without modifying code.
