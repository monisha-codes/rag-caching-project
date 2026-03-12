from .models import Document
from .embeddings import get_embedding


def ingest_documents(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        docs = f.read().split("\n\n")

    for doc in docs:

        if doc.strip():

            embedding = get_embedding(doc)

            Document.objects.create(
                content=doc,
                embedding=embedding
            )

    print("Documents loaded successfully")