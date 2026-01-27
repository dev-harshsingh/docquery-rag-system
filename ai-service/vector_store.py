from langchain_community.vectorstores import FAISS
import os

def build_faiss_index(chunks, embedding_model):
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )
    return vector_store


def save_faiss_index(vector_store, path="faiss_index"):
    vector_store.save_local(path)


def load_faiss_index(embedding_model, path="faiss_index"):
    return FAISS.load_local(
        path,
        embedding_model,
        allow_dangerous_deserialization=True
    )


INDEX_PATH = "faiss_index"

def add_documents_to_faiss(chunks, embedding_model):
    if os.path.exists(INDEX_PATH):
        vector_store = FAISS.load_local(
            INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embedding_model
        )

    vector_store.save_local(INDEX_PATH)
