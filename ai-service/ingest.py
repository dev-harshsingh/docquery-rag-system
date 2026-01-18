import os
from langchain_community.document_loaders import ( 
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
def load_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌File is missing")
    if file_path.endswith(".pdf"):
        loader=PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader=Docx2txtLoader(file_path)
    elif file_path.endswith(".txt"):
        loader=TextLoader(file_path)
    else:
        raise ValueError("❌ File type not supported")
    documents=loader.load() 
    return documents