import redis
import numpy as np
from sentence_transformers import SentenceTransformer

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Check if index already exists
index_exists = r.execute_command("FT._LIST") == [b'questions']
# Create an index in Redis for storing questions and their embeddings if needed
if index_exists is False:
    r.execute_command("FT.CREATE", "questions", "ON", "hash", "SCHEMA", "id", "NUMERIC", "question", "TEXT", "embedding", "VECTOR", "HNSW", "6", "TYPE", "FLOAT32", "DIM", "768", "DISTANCE_METRIC", "COSINE")

model = SentenceTransformer('paraphrase-distilroberta-base-v1')

# List of questions to create embeddings for
questions = [
    "What is the capital of France?",
    "How do I create a Slack bot?",
    "What are the health benefits of exercise?"
]

# Generate and store embeddings
for idx, question in enumerate(questions):
    embedding = model.encode(question, convert_to_numpy=True).astype(np.float32).tobytes()
    print(f"Storing document question:{idx}")
    # Store the question and its embedding in Redis
    r.hset(f"question:{idx}", mapping = {"id": idx, "question": question, "embedding": embedding})
