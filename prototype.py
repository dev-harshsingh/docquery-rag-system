import os
from langchain_community.document_loaders import ( PyPDFLoader, TextLoader, Docx2txtLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai
from dotenv import load_dotenv

path='data'

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)




docs=[]    
for doc in os.listdir(path):
    fpath=os.path.join(path,doc)
    if doc.endswith(".pdf"):
        loader=PyPDFLoader(fpath)
    elif doc.endswith(".docx"):
        loader=Docx2txtLoader(fpath)
    elif doc.endswith(".txt"):
        loader = TextLoader(fpath)
    else:
        continue

    loader_docs=loader.load()
    docs.extend(loader_docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(docs)

embeddings=HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"

)

vector = embeddings.embed_query(chunks[0].page_content)


vectoreStore=FAISS.from_documents(
    chunks,
    embedding=embeddings
)
    
while(True):
    query=input(("Enter your query..."))
    if query.lower()=="exit":
        break
    results=vectoreStore.similarity_search(query,k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"""You are an assistant that answers questions ONLY using the context below.
    If the answer is not present in the context, say "I don't know".Context:{context} Question:{query} Answer in clear and simple language:"""
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,)
    print("\nAnswer (from documents):")
    print(response.text)
    print("-" * 40)
