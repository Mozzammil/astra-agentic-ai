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