from fastapi import FastAPI
from pydantic import BaseModel
from embeddings import embed_text
from faiss_index import search

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Docs Q&A API")

class Query(BaseModel):
    question: str

# Assume `docs` list exists from load_docs.py
from load_docs import docs

@app.post("/query")
def query_docs(q: Query):
    q_vector = embed_text(q.question)
    top_indices, distances = search(q_vector, k=3)

    context = "\n".join([docs[i] for i in top_indices])

    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "Answer based on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q.question}"}
        ],
        max_tokens=200
    )

    answer = response['choices'][0]['message']['content']
    return {"answer": answer, "context_docs": top_indices.tolist()}
