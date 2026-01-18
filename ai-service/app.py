from flask import Flask, request, jsonify
from ingest import load_document
from chunking import chunk_document
from embeddings import embed_chunks,get_embedding_model

embedding_model = get_embedding_model()

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/ingest", methods=["POST"])
def ingest_document():
    data = request.get_json()

    if not data or "file_path" not in data:
        return jsonify({"error": "❌file_path is required"}), 400

    file_path = data["file_path"]

    try:
        documents = load_document(file_path)
        chunks=chunk_document(documents)
        vectors=embed_chunks(chunks,embedding_model)
        
        total_chars = sum(len(doc.page_content) for doc in documents)  
        print(f"📁 file uploaded Sucessfully: {file_path}")
        return jsonify({
            "message": "Document loaded successfully",
            "pages": len(documents),
            "total_characters": total_chars,
            "avg_chunk_size": sum(len(c.page_content) for c in chunks) // len(chunks),
            "dimensions": len(vectors[0])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
