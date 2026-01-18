from flask import Flask, request, jsonify
from ingest import load_document
from chunking import chunk_document
from embeddings import get_embedding_model
from vector_store import build_faiss_index,save_faiss_index, load_faiss_index
from llm import generate_answer


embedding_model = get_embedding_model()
app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


# MAIN CODE

@app.route("/ingest", methods=["POST"])
def ingest_document():
    data = request.get_json()

    if not data or "file_path" not in data:
        return jsonify({"error": "❌file_path is required"}), 400

    file_path = data["file_path"]

    try:
        #load docs
        documents = load_document(file_path)
        #break into  chunks
        chunks=chunk_document(documents)
        # FAISS Indexing
        vector_store = build_faiss_index(chunks, embedding_model)
        #save to local
        save_faiss_index(vector_store)

        total_chars = sum(len(doc.page_content) for doc in documents)  
        print(f"📁 File indexed successfully: {file_path}")

        return jsonify({
            "message": "Document indexed successfully",
            "pages": len(documents),
            "chunks": len(chunks)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
from vector_store import load_faiss_index

#ask question
@app.route("/query", methods=["POST"])
def query_document():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "❌ question is required"}), 400

    question = data["question"]

    try:
        #  Load FAISS index
        vector_store = load_faiss_index(embedding_model)

        # Retrieve relevant chunks
        docs = vector_store.similarity_search(
            query=question,
            k=3
        )

        context_chunks = [doc.page_content for doc in docs]

        # Generate answer using Gemini
        answer = generate_answer(context_chunks, question)

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "source": doc.metadata.get("source")
                }
                for doc in docs
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
