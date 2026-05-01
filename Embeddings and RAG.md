# 📚 Day 17 — Embeddings & RAG (Retrieval-Augmented Generation)

---

## 🎯 Objective

Enable Astra to:

* Store knowledge from files
* Retrieve relevant context
* Answer questions from large documents

---

## 🧠 What We Built

```text
File → Chunk → Embeddings → Vector Store → Retrieval → LLM Answer
```

👉 Astra is now a **knowledge-aware AI system**

---

# ⚙️ Step 1 — Install Dependencies

```bash
pip install langchain
pip install langchain-community
pip install faiss-cpu
```

---

# ⚙️ Step 2 — Setup Embedding Model

### Pull embedding model (IMPORTANT)

```bash
ollama pull nomic-embed-text
```

### Verify

```bash
ollama list
```

---

## 📁 `core/rag/embeddings.py`

```python
from langchain_community.embeddings import OllamaEmbeddings

def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")
```

---

# ⚙️ Step 3 — Vector Store (FAISS)

---

## 📁 `core/rag/vector_store.py`

```python
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from core.rag.embeddings import get_embeddings


class VectorStore:
    def __init__(self):
        self.embedding = get_embeddings()
        self.store = None

    def add_texts(self, texts):
        docs = [Document(page_content=t) for t in texts]

        if self.store is None:
            self.store = FAISS.from_documents(docs, self.embedding)
        else:
            self.store.add_documents(docs)

    def search(self, query, k=2):
        if not self.store:
            return []

        results = self.store.similarity_search(query, k=k)
        return [r.page_content for r in results]
```

---

# ⚙️ Step 4 — Text Chunking

---

## 📁 `core/rag/chunker.py`

```python
def chunk_text(text, chunk_size=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks
```

---

# ⚙️ Step 5 — RAG Pipeline

---

## 📁 `core/rag/rag_pipeline.py`

```python
from core.rag.vector_store import VectorStore
from core.rag.chunker import chunk_text

vector_db = VectorStore()

def index_text(text):
    chunks = chunk_text(text)
    vector_db.add_texts(chunks)

def retrieve(query):
    return vector_db.search(query)
```

---

# ⚙️ Step 6 — Integrate with Agent

---

## 📁 `agent_service.py`

### 1. Import RAG

```python
from core.rag.rag_pipeline import index_text, retrieve
```

---

### 2. Index after file read

```python
if action == "file_reader":
    content = result.get("content", "")
    if content:
        print("📥 Indexing content into vector DB")
        index_text(content)
```

---

### 3. Retrieve before LLM call

```python
retrieved_chunks = retrieve(question)

if retrieved_chunks:
    print("📚 Retrieved context:", retrieved_chunks)

    scratchpad += f"""
Relevant context:
{retrieved_chunks}
"""
```

---

# 🧪 Step 7 — Testing

---

## Test 1 — Index File

```text
Analyze file sample.txt
```

✅ Should:

* Read file
* Chunk text
* Store embeddings in FAISS

---

## Test 2 — Ask Question

```text
What is microservices architecture?
```

✅ Should:

* Retrieve relevant chunks 📚
* Answer using that context

---

## Test 3 — Memory vs RAG

```text
What are key points?
```

✅ Should:

* Use memory (not RAG)

---

# 🧠 Key Learnings

---

## 🔹 Memory vs RAG

| Feature | Memory       | RAG       |
| ------- | ------------ | --------- |
| Size    | Small        | Large     |
| Speed   | Fast         | Medium    |
| Purpose | Conversation | Knowledge |

---

## 🔹 Why RAG?

LLMs don’t store your data.

👉 RAG allows:

* External knowledge
* Scalable intelligence
* Document understanding

---

## 🔹 Embeddings

* Convert text → vectors
* Similar meaning → similar vectors
* Enables semantic search

---

# 🚀 Outcome

Astra can now:

* 📄 Read files
* 🧠 Store knowledge
* 🔍 Search relevant context
* 💬 Answer from documents

---

# 🔥 System Evolution

```text
Basic LLM ❌
Agent ❌
Agent + Memory ❌
Agent + Memory + RAG ✅
```

---

# ⚠️ Common Issues & Fixes

---

### ❌ Error: `model "nomic-embed-text" not found`

```bash
ollama pull nomic-embed-text
```

---

### ❌ Error: `langchain.vectorstores not found`

Use:

```python
from langchain_community.vectorstores import FAISS
```

---

# 🔜 Next Step

## 🚀 Day 18 — RAG + Agent Fusion

👉 Astra will decide:

* When to use Memory
* When to use RAG
* When to use Tools

---

# 🧠 Final Insight

> Tools make agents capable
> Memory makes them conversational
> RAG makes them knowledgeable

👉 You now have all three.
