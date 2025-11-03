from sentence_transformers import SentenceTransformer

# Use a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """Return a vector embedding of the text"""
    return model.encode(text)
