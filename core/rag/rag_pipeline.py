from core.rag.vector_store import VectorStore
from core.rag.chunker import chunk_text

vector_db = VectorStore()

def index_text(text):
    chunks = chunk_text(text)
    vector_db.add_texts(chunks)

def retrieve(query):
    return vector_db.search(query)