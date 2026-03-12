import redis
import hashlib
import numpy as np
import json
from .embeddings import get_embedding

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def get_cache_key(query):
    return "answer:" + hashlib.md5(query.encode()).hexdigest()


def get_kv_cache(query):

    key = get_cache_key(query)

    result = redis_client.get(key)

    if result:
        return result.decode()

    return None


def set_kv_cache(query, answer):

    key = get_cache_key(query)

    redis_client.set(key, answer, ex=3600)



def cosine(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))


def semantic_cache_lookup(query):

    query_emb = get_embedding(query)

    keys = redis_client.keys("semantic:*")

    for k in keys:

        data = json.loads(redis_client.get(k))

        stored_emb = data["embedding"]

        score = cosine(query_emb, stored_emb)

        if score > 0.95:
            return data["answer"]

    return None


def store_semantic_cache(query, answer):

    emb = get_embedding(query)

    data = {
        "embedding": emb,
        "answer": answer
    }

    redis_client.set(
        "semantic:" + query,
        json.dumps(data),
        ex=3600
    )