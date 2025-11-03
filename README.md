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
  main.py              # FastAPI app exposing /query
docs/
  *.txt                # your source documents
```

### Prerequisites
- Python 3.10+
- Internet access to download the embedding model and FAISS wheels
- An OpenAI API key (set `OPENAI_API_KEY`)

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

### Run the API
uvicorn will start the FastAPI app and the `load_docs.py` import will build the FAISS index at startup.
```bash
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`. Open the interactive docs at `http://127.0.0.1:8000/docs`.

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

### Notes
- Windows FAISS: `requirements.txt` includes a Windows-compatible wheel source and conditional pins.
- Embedding model: `all-MiniLM-L6-v2` (384-dim). Make sure `DIM` in `faiss_index.py` matches.
- Startup behavior: `load_docs.py` runs at import time, embedding all files under `docs/` and building the index. Restart the server after changing documents.

### Development Tips
- If you add many/large docs, consider chunking and caching embeddings.
- Handle empty or missing `docs/` gracefully if you extend the app.

### License
MIT (add your preferred license here).


