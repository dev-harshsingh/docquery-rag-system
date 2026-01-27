import redis
import json

from ingest import load_document
from chunking import chunk_document
from embeddings import get_embedding_model
from vector_store import add_documents_to_faiss

# Redis config
REDIS_HOST = "localhost"
REDIS_PORT = 6379
QUEUE_NAME = "ingest_queue"

# Initialize Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Load embedding model ONCE
embedding_model = get_embedding_model()

print("🟢 Ingestion worker started. Waiting for jobs...")

while True:
    try:
        # Block until a job is available
        _, job = redis_client.brpop(QUEUE_NAME)

        print("📥 Job received:", job)

        # Parse job payload
        job_data = json.loads(job)
        file_path = job_data.get("file_path")

        if not file_path:
            print("❌ Invalid job payload, missing file_path")
            continue

        # 1️⃣ Load document
        documents = load_document(file_path)

        # 2️⃣ Chunk document
        chunks = chunk_document(documents)

        # 3️⃣ Add chunks to FAISS
        add_documents_to_faiss(chunks, embedding_model)

        print(f"✅ Successfully ingested: {file_path}")

    except Exception as e:
        print("🔥 Error processing job:", str(e))
