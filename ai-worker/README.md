# MediGuide AI Worker

Python AI/document-processing worker for the MediGuide platform.

It processes uploaded clinical guideline PDFs and Markdown files into:

- cleaned HTML
- Markdown
- structured sections
- extracted tables
- searchable chunks
- vector embeddings for `guideline_chunks.embedding`
- RAG answers with citations

This project is designed to plug into the Go backend scaffold generated earlier.

## Features

- FastAPI service for health checks, manual job runs, extraction preview, embeddings, and RAG answers
- Background worker that polls `ingestion_jobs` from PostgreSQL
- MinIO/S3 file download and upload
- PDF extraction using PyMuPDF and optional pdfplumber
- UTF-8 Markdown parsing with heading hierarchy, lists, callouts, and GFM tables
- HTML cleaning using BeautifulSoup
- Section detection from PDF heading/font structure
- Chunking with overlap
- pgvector-compatible embeddings
- Optional providers:
  - deterministic local hash embeddings for development
  - Ollama embeddings
  - SentenceTransformers embeddings
  - OpenAI embeddings
  - Ollama generation
  - OpenAI generation
- Safe RAG prompt that answers only from retrieved guideline chunks
- Notebooks for experimentation
- Dockerfile and docker-compose override

## Quick start

```bash
cd ai-worker
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8090
```

Pull the default response and embedding models before running ingestion or RAG:

```bash
ollama pull mxbai-embed-large:latest
ollama pull gemma3:4b
```

If you switch `EMBEDDING_PROVIDER=sentence_transformers`, install the optional model stack separately:

```bash
pip install sentence-transformers
```

Run the worker loop:

```bash
python -m app.worker
```

Run tests:

```bash
pytest
```

## Docker

From the repo root:

```bash
make up
make ps
```

The AI HTTP (`8090`) and gRPC (`50051`) ports remain internal to the Compose
network. Infrastructure and host-port ownership live only in `infra`.

## Integration with Go backend

The Go backend creates rows in `ingestion_jobs` after a guideline PDF/Markdown upload or a
Markdown editor save.

The worker polls jobs with:

```sql
status = 'queued'
job_type IN ('pdf_ingestion', 'markdown_ingestion')
```

For each job, it:

1. Reads the immutable source key from the job payload and validates that it is still current.
2. Downloads the PDF or Markdown source from MinIO.
3. Extracts or parses text, hierarchy, typed blocks, HTML, and Markdown.
4. Stores HTML and Markdown back to MinIO
5. Inserts records into:
   - `guideline_sections`
   - `guideline_chunks`
   - `guideline_tables`
6. Updates `guideline_versions.html_file_key` and `markdown_file_key`
7. Marks the job as `completed`

Superseded Markdown jobs exit without overwriting a newer edit. Markdown-only guidelines have no
PDF page provenance; the worker records that limitation in extraction metadata and warnings.

## Recommended first production mode

For clinical safety, start with:

```env
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=mxbai-embed-large:latest
EMBEDDING_DIM=1024
LLM_PROVIDER=ollama
OLLAMA_MODEL=gemma3:4b
```

For lightweight development without model downloads:

```env
EMBEDDING_PROVIDER=hash
EMBEDDING_DIM=1024
LLM_PROVIDER=extractive
```

## Important clinical safety rule

Every agent uses strict document excerpts from retrieved, approved chunks of the
current published documents (including ingested PDFs). Gemma selects source
numbers and fixed section headings; the server inserts complete source passages
and builds citations from stored metadata. Model-authored factual prose is never
displayed. This deliberately limits writing/report output to organized quotations,
rather than free-form paraphrases or translations.

Selections with invented source numbers, extra prose, invalid structure, or no
support return an insufficient-evidence response with no citations and
`grounded=false`. Generation failures also fail closed. Previous chat answers and
user assertions are never used as factual evidence. The backend preserves worker
refusals; its local search path returns only labelled source snippets.

This prevents the model from adding unsupported claims, but source correctness,
PDF extraction accuracy, completeness of retrieved context, and passage relevance
still require review. It is not a guarantee that every selected passage answers
every part of a clinical question.

## Response agents

Ollama uses `gemma3:4b` by default. Set `OLLAMA_MODEL` to use another installed
model. The embedding model stays `mxbai-embed-large:latest`, so switching the
response model does not require reindexing existing documents. `make up` pulls
the configured models and rebuilds the AI worker.

The existing RAG endpoint automatically selects a response agent from the request:

| Request | Agent | Output |
| --- | --- | --- |
| “What are the signs of malaria?” | Clinical | Relevant document excerpts with source citations |
| “Write a patient handout about malaria prevention” | Writing | Source excerpts organized under Draft |
| “Prepare a report on malaria prevention” | Report | Source excerpts organized into supported report sections |

Revisions such as “Make it shorter” retain the previous user's requested agent;
a new clinical question returns to clinical Q&A. Routing is deterministic and
adds no model request. Each agent supplies its own instructions to the configured
generation provider. Writing and report agents can use up to six retrieved
chunks; clinical answers use up to three. The selected agent is recorded in
the worker HTTP response's `safety.agent` field.

All agents use the same evidence checks and citation handling. Reports use
indexed guidance, not live facility analytics. Requests requiring counts, dates,
patient details, or outcomes absent from the documents must be declined.
`LLM_PROVIDER=extractive` selects and displays complete retrieved passages
without a model call, under an Evidence heading. The HTTP response records
`safety.grounding_mode=document_excerpts`; this describes source provenance,
not a clinical correctness assessment.
