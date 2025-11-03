import os
from .embeddings import embed_text
from .faiss_index import add_vectors

docs_folder = "docs"
docs = []

vectors = []

for filename in os.listdir(docs_folder):
    path = os.path.join(docs_folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        docs.append(text)
        vectors.append(embed_text(text))

add_vectors(vectors)

print("FAISS index ready! Number of documents:", len(docs))
