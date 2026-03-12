from sentence_transformers import SentenceTransformer

# Load lightweight local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()