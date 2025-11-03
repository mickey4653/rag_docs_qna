from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .embeddings import embed_text
from .faiss_index import search

from openai import OpenAI, APIError, RateLimitError, AuthenticationError
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # uses OPENAI_API_KEY from environment

app = FastAPI(title="Docs Q&A API")

class Query(BaseModel):
    question: str

# Assume `docs` list exists from load_docs.py
from .load_docs import docs

@app.get("/")
def root():
    return {"status": "ok", "endpoints": ["GET /health", "POST /query", "GET /docs"]}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/query")
def query_docs(q: Query):
    q_vector = embed_text(q.question)
    top_indices, distances = search(q_vector, k=3)

    # ensure list for JSON serialization
    top_list = top_indices.tolist() if hasattr(top_indices, "tolist") else list(top_indices)
    context = "\n".join([docs[i] for i in top_list])

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer based on the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q.question}"}
            ],
            max_tokens=200
        )
    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit/quota exceeded. Check plan and billing.")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="OpenAI authentication failed. Check OPENAI_API_KEY.")
    except APIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")

    answer = completion.choices[0].message.content
    return {"answer": answer, "context_docs": top_list}
