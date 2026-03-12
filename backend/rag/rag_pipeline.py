import numpy as np
from .models import Document
from .embeddings import get_embedding
from .cache import get_kv_cache, set_kv_cache
from .cache import semantic_cache_lookup, store_semantic_cache


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_documents(query):

    query_embedding = get_embedding(query)

    docs = Document.objects.all()

    scored = []

    for d in docs:
        score = cosine_similarity(query_embedding, d.embedding)
        scored.append((score, d.content))

    scored.sort(reverse=True)

    top_docs = [doc for _, doc in scored[:3]]

    return top_docs


def generate_answer(question, docs):
    """
    Simple generator using retrieved context.
    This avoids OpenAI API quota issues while still demonstrating RAG.
    """

    context = "\n\n".join(docs)

    if not context:
        return "No relevant documents found."

    answer = f"""Based on the retrieved documents:

{context}

Question: {question}
"""

    return answer


def rag_pipeline(query):

    # 1️⃣ KV cache check
    cached = get_kv_cache(query)

    if cached:
        return cached, True

    # 2️⃣ Semantic cache check
    semantic = semantic_cache_lookup(query)

    if semantic:
        return semantic, True

    # 3️⃣ Retrieve documents
    docs = retrieve_documents(query)

    # 4️⃣ Generate answer
    answer = generate_answer(query, docs)

    # 5️⃣ Store in caches
    set_kv_cache(query, answer)
    store_semantic_cache(query, answer)

    return answer, False