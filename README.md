## RAG Docs Q&A

A simple Retrieval-Augmented Generation (RAG) API built with FastAPI. It indexes plain-text files from the `docs` folder using FAISS and answers questions by retrieving the most relevant documents and generating answers with an LLM.

### Features
- Indexes documents in `docs/` using `sentence-transformers` embeddings and FAISS
- FastAPI endpoint to query your knowledge base
- Configurable via `OPENAI_API_KEY` from `.env`

### Project Structure
```
app/
  embeddings.py        # loads sentence-transformers model and creates embeddings
  faiss_index.py       # FAISS index helpers (add/search)
  load_docs.py         # loads docs/, embeds, and builds the index
  main.py              # FastAPI app exposing /, /health, /query
docs/
  *.txt                # your source documents
```

### Prerequisites
- Python 3.10+
- Internet access to download the embedding model and FAISS wheels
- An OpenAI API key (set `OPENAI_API_KEY`)
  - Ensure your OpenAI account has an active plan/credits to avoid 429 insufficient_quota errors

### Installation
1. Create and activate a virtual environment (recommended)
   - Windows (PowerShell):
     ```bash
     python -m venv .venv
     .venv\\Scripts\\Activate.ps1
     ```
   - Git Bash:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Add Documents
Place your `.txt` files in the `docs/` folder. Each file is treated as a single document.

### Run the API (local)
uvicorn will start the FastAPI app and the `load_docs.py` import will build the FAISS index at startup.
```bash
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`. Open the interactive docs at `http://127.0.0.1:8000/docs`.
Useful endpoints:
- `GET /` basic status
- `GET /health` health check
- `POST /query` ask a question

### Run with Docker
Build the image:
```bash
docker build -t rag-docs-qna .
```

Run the container (pass your API key and mount `docs/` so you can edit without rebuilding):
```bash
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/docs:/app/docs \
  rag-docs-qna
```

On Windows PowerShell, use:
```powershell
docker run --rm -p 8000:8000 `
  -e OPENAI_API_KEY=$Env:OPENAI_API_KEY `
  -v ${PWD}/docs:/app/docs `
  rag-docs-qna
```

### Query the API
POST `http://127.0.0.1:8000/query`
Request body:
```json
{ "question": "What is NLP?" }
```
Response:
```json
{
  "answer": "...generated answer...",
  "context_docs": [0, 2, 3]
}
```

If you see HTTP 429 with details about quota, add credits to your OpenAI account or reduce request volume. The server maps common OpenAI errors to HTTP responses (401 auth, 429 quota, 502 upstream errors) instead of returning a generic 500.

### Notes
- Windows FAISS: `requirements.txt` includes a Windows-compatible wheel source and conditional pins.
- Embedding model: `all-MiniLM-L6-v2` (384-dim). Make sure `DIM` in `faiss_index.py` matches.
- Startup behavior: `load_docs.py` runs at import time, embedding all files under `docs/` and building the index. Restart the server after changing documents.
 - Docker: `.dockerignore` excludes common local-only files (including `.env`). Provide `OPENAI_API_KEY` with `-e` when running the container.

### Dependencies
Key versions (see `requirements.txt`):
- `sentence-transformers==2.3.0`
- `openai>=1.51.0` (uses the new `OpenAI` client)
- `httpx>=0.24.0`

### Development Tips
- If you add many/large docs, consider chunking and caching embeddings.
- Handle empty or missing `docs/` gracefully if you extend the app.

### License
MIT (add your preferred license here).


