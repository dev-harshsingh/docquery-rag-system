from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    embeddings=HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return embeddings
def embed_chunks(chunks, embedding_model):
    texts = [chunk.page_content for chunk in chunks]
    vectors = embedding_model.embed_documents(texts)
    return vectors