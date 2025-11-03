import faiss
import numpy as np

# dimension must match embedding size
DIM = 384  # MiniLM-L6-v2 outputs 384-d vectors

index = faiss.IndexFlatL2(DIM)

def add_vectors(vectors):
    """vectors: list of numpy arrays"""
    index.add(np.array(vectors, dtype='float32'))

def search(query_vector, k=3):
    """Return top k results"""
    distances, indices = index.search(np.array([query_vector], dtype='float32'), k)
    return indices[0], distances[0]
