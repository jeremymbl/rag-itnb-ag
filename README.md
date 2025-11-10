# ITNB RAG Pipeline

> **Note:** This project was developed as part of the technical interview process for ITNB AG, demonstrating RAG implementation capabilities and understanding of their product ecosystem.

A Retrieval-Augmented Generation (RAG) system for intelligent question-answering over ITNB website content. This pipeline crawls, indexes, and enables natural language interactions with information about ITNB's products, services, and solutions.

## About ITNB

**ITNB AG** is a Swiss technology company specializing in:
- **Sovereign Cloud** - Swiss-based, privacy-focused infrastructure (IaaS)
- **AI/ML Services** - AI Model as a Service, GPU infrastructure
- **Cybersecurity** - SOC as a Service, Endpoint Security, SIEM
- **Professional Services** - Project management, AI consulting

Their motto is "Safe, Secure, Swiss" - emphasizing data sovereignty, compliance with Swiss regulations, and independence from foreign cloud providers.

## Features

- **Automated Web Crawling** - Crawls ITNB website using async crawl4ai with BFS traversal
- **Text Processing** - Converts markdown to clean plain text suitable for embedding
- **Vector Database Integration** - Stores and searches documents using GroundX
- **Interactive Chat Interface** - Command-line Q&A system with source citations
- **LLM Integration** - OpenAI-compatible API for answer generation
- **Configurable Pipeline** - Environment-based configuration for easy deployment

## Architecture

The system follows a classic RAG (Retrieval-Augmented Generation) pattern:

```
┌─────────────────┐
│  ITNB Website   │
│  (itnb.ch/en)   │
└────────┬────────┘
         │ crawl4ai
         ▼
┌─────────────────┐
│   Preprocess    │ ← text_processing.py
│  (markdown→txt) │
└────────┬────────┘
         │ data/itnb_texts.json
         ▼
┌─────────────────┐
│  GroundX Ingest │ ← groundx_utils.py
│ (vector storage)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  User Question  │────▶│ GroundX      │
└─────────────────┘     │ Search (K=3) │
                        └──────┬───────┘
                               │ context
                               ▼
                        ┌──────────────┐
                        │ LLM Generate │
                        │(with context)│
                        └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │Answer+Sources│
                        └──────────────┘
```

## Prerequisites

- **Python 3.8+**
- **GroundX API Key** - Sign up at [GroundX](https://www.groundx.ai/)
- **OpenAI-Compatible LLM API** - Any OpenAI-compatible endpoint (OpenAI, ITNB MaaS, etc.)

## Installation

1. Clone the repository:
```bash
# HTTPS
git clone https://github.com/jeremymbl/rag-itnb-ag.git
cd rag-itnb-ag

# Or with SSH
git clone git@github.com:jeremymbl/rag-itnb-ag.git
cd rag-itnb-ag

# Or with GitHub CLI
gh repo clone jeremymbl/rag-itnb-ag
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your API credentials:
```bash
# GroundX Configuration
GROUNDX_API_KEY=your_groundx_api_key_here
GROUNDX_BUCKET_NAME=itnb_website

# OpenAI-Compatible LLM Configuration
OPENAI_API_KEY=your_llm_api_key_here
OPENAI_API_BASE=https://api.openai.com  # Or your LLM provider URL
OPENAI_MODEL_NAME=gpt-4  # Or your model name
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `GROUNDX_API_KEY` | *(required)* | Your GroundX API key |
| `GROUNDX_BUCKET_NAME` | `itnb_website` | GroundX bucket name for document storage |
| `OPENAI_API_KEY` | *(required)* | LLM API key |
| `OPENAI_API_BASE` | *(required)* | Base URL for OpenAI-compatible API |
| `OPENAI_MODEL_NAME` | *(required)* | Model name to use for generation |
| `CRAWL_START_URL` | `https://www.itnb.ch/en` | Starting URL for crawler |
| `CRAWL_MAX_DEPTH` | `2` | Maximum crawl depth (BFS) |
| `CRAWL_MAX_PAGES` | `100` | Maximum pages to crawl |
| `LLM_MAX_TOKENS` | `512` | Max tokens for LLM response |
| `LLM_TEMPERATURE` | `0.0` | LLM temperature (0.0 = deterministic) |
| `TOP_K` | `3` | Number of search results to retrieve |

## Usage

### Step 1: Crawl the ITNB Website

```bash
python -m itnb_rag.preprocess
```

This will:
- Crawl pages starting from `https://www.itnb.ch/en`
- Extract and clean markdown content
- Save results to `data/itnb_texts.json` (structured) and `data/itnb_corpus.txt` (flat)

**Output:**
```
Starting crawl from https://www.itnb.ch/en ...
Crawled 37 pages successfully.
Saved data/itnb_texts.json
Saved data/itnb_corpus.txt
```

### Step 2: Ingest Documents to GroundX

```bash
python -m itnb_rag.ingest
```

This will:
- Load documents from `data/itnb_texts.json`
- Create or find the GroundX bucket
- Upload each document for embedding and indexing
- Log results to `data/ingest_log.txt`

**Output:**
```
GroundX bucket 'itnb_website' found/created with ID: 12345
Ingesting 37 documents...
✓ https://www.itnb.ch/en (200)
✓ https://www.itnb.ch/en/products-and-services/... (200)
...
Ingestion complete. Check data/ingest_log.txt for details.
```

### Step 3: Start Interactive Chat

```bash
python -m itnb_rag.chat
```

This will start an interactive prompt where you can ask questions:

```
Looking up bucket 'itnb_website'...
Found bucket: 22745
Using bucket id: 22745
Using LLM model: inference-llama4-maverick @ https://maas.ai-2.kvant.cloud

ITNB RAG CLI — ask questions about the ingested ITNB content.
Commands: /help /exit /quit /raw (shows raw combined context)

itnb> What is ITNB's Sovereign Cloud?

[1/2] Retrieved context length: 79,332 chars
[2/2] Sending to LLM... (this may take a few seconds)

--- Answer ---

ITNB's Sovereign Cloud is a secure, Swiss-hosted infrastructure that ensures full data sovereignty, compliance, and high performance for sensitive workloads across various sectors, including artificial intelligence (AI), finance, healthcare, and government. It is designed to provide a reliable and secure infrastructure-as-a-service (IaaS) solution, with data centers located in Zurich and Basel, guaranteeing a 99.99% uptime. The Sovereign Cloud offers CPU and GPU computing, storage solutions, and networking capabilities, all tailored for sensitive workloads.

Sources:
- www.itnb.ch_en_solutions_industries_education-and-research.txt
- www.itnb.ch_en_products-and-services_infrastructure-as-a-service_sovereign-cloud.txt

--- End Answer ---

Sources used:
 [1] Education and Research — https://www.itnb.ch/en/solutions/industries/education-and-research (score=560.0113)
 [2] Sovereign Cloud — https://www.itnb.ch/en/products-and-services/infrastructure-as-a-service/sovereign-cloud (score=555.7248)
 [3] Education and Research — https://www.itnb.ch/en/solutions/industries/education-and-research (score=544.65515)
itnb> /exit
Bye.
```

### Chat Commands

- `/help` - Show available commands
- `/exit` or `/quit` - Exit the chat
- `/raw` - Display the raw context retrieved for the last query
- Any other text - Ask a question about ITNB

## Project Structure

```
rag-itnb-ag/
├── itnb_rag/                   # Main Python package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # CLI help/usage information
│   ├── config.py               # Centralized configuration management
│   ├── preprocess.py           # Web crawler (crawl4ai integration)
│   ├── text_processing.py      # Markdown to plain text conversion
│   ├── groundx_utils.py        # GroundX API helper functions
│   ├── ingest.py               # Document ingestion to GroundX
│   └── chat.py                 # Interactive RAG chat interface
├── data/                       # Generated data (git-ignored)
│   ├── itnb_texts.json         # Crawled documents (37 pages)
│   ├── itnb_corpus.txt         # Flat text corpus
│   └── ingest_log.txt          # Ingestion results log
├── .env                        # Environment variables (git-ignored)
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── README.md                   # This file
```

## How It Works

### 1. Preprocessing (`itnb_rag/preprocess.py`)

**Purpose:** Crawl and extract clean text from the ITNB website.

**Implementation:**
- Uses **crawl4ai** for async web crawling
- Implements **BFS (Breadth-First Search)** with configurable depth limit
- Filters: Only `/en` pages, only HTML content
- Extracts markdown using `LXMLWebScrapingStrategy`
- Converts markdown → HTML → plain text using `mistune` + `BeautifulSoup`
- Normalizes whitespace and removes formatting artifacts

**Key Functions:**
- `crawl_and_save()` - Main crawling orchestrator
- `md_to_text()` - Markdown to text conversion (from `text_processing.py`)

### 2. Ingestion (`itnb_rag/ingest.py`)

**Purpose:** Upload preprocessed documents to GroundX vector database.

**Implementation:**
- Connects to GroundX API
- Creates or retrieves bucket by name
- Ingests each document with metadata:
  - `url` - Source URL
  - `title` - Page title
  - `ingested_at` - Timestamp
- GroundX automatically:
  - Fetches content from URL
  - Generates embeddings
  - Stores in vector database

**Key Functions:**
- `get_client()` - Initialize GroundX client
- `get_bucket_id()` - Get or create bucket
- `ingest_document()` - Upload single document

### 3. Chat Interface (`itnb_rag/chat.py`)

**Purpose:** Interactive Q&A system using RAG pattern.

**Implementation:**

**Retrieval Phase:**
1. User submits question
2. Perform semantic search in GroundX (returns top K=3 results)
3. Extract combined context text and source metadata

**Generation Phase:**
1. Build system prompt with embedded context
2. Truncate context if too large (>20,000 chars)
3. Send to OpenAI-compatible LLM API
4. Parse and display answer
5. Show source citations with URLs and relevance scores

**Key Functions:**
- `retrieve_context()` - Search GroundX for relevant documents
- `build_system_instruction()` - Construct prompt with context
- `call_llm()` - Send request to LLM API
- `interactive_loop()` - Main chat REPL

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **crawl4ai** | Async web crawler with markdown extraction |
| **GroundX SDK** | Vector database for document storage and semantic search |
| **mistune** | Markdown parser (MD → HTML conversion) |
| **BeautifulSoup4** | HTML parsing and text extraction |
| **requests** | HTTP client for LLM API calls |
| **python-dotenv** | Environment variable management |

## Known Issues

### GroundX Token Limit (402 Error)

The ingestion process may fail with a 402 status code:

```
Your subscription limits you to a maximum of 5000000 ingested tokens per month
```

**Solutions:**
1. Upgrade your GroundX subscription plan
2. Wait until your monthly token quota resets
3. Reduce the number of pages crawled by adjusting `CRAWL_MAX_PAGES` in `.env`

### Empty Search Results

If the chat returns "no context found":
- Verify documents were successfully ingested (check `data/ingest_log.txt`)
- Ensure the GroundX bucket name matches in `.env`
- Try rephrasing your question

## Troubleshooting

### Import Errors

```bash
ModuleNotFoundError: No module named 'crawl4ai'
```

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### API Key Errors

```
ValueError: GROUNDX_API_KEY not set in environment
```

**Solution:** Verify `.env` file exists and contains valid API keys:
```bash
cat .env  # Check file contents
```

### Timeout Errors

```
requests.exceptions.Timeout: HTTPSConnectionPool
```

**Solution:** Increase timeout in `config.py` or check network connectivity:
```python
REQUEST_TIMEOUT: int = 120  # Increase from 60 to 120 seconds
```

## Development

### Running Individual Modules

```bash
# Show usage information
python -m itnb_rag

# Run preprocessor
python -m itnb_rag.preprocess

# Run ingestion
python -m itnb_rag.ingest

# Run chat interface
python -m itnb_rag.chat
```

### Customizing the Crawler

Edit `itnb_rag/config.py`:
```python
# Crawl more pages
CRAWL_MAX_PAGES: int = 200

# Crawl deeper
CRAWL_MAX_DEPTH: int = 3

# Change starting URL
CRAWL_START_URL: str = "https://example.com"
```

### Customizing LLM Behavior

Edit `itnb_rag/config.py`:
```python
# More creative responses
LLM_TEMPERATURE: float = 0.7

# Longer responses
LLM_MAX_TOKENS: int = 1024

# More context
TOP_K: int = 5
```

## Future Improvements

- [ ] Add unit tests for text processing
- [ ] Implement incremental crawling (update only changed pages)
- [ ] Add conversation history/memory to chat
- [ ] Create web UI (Streamlit/Gradio)
- [ ] Add support for multiple languages
- [ ] Implement caching for LLM responses
- [ ] Add metrics/analytics (query latency, search accuracy)
- [ ] Support document upload (PDFs, docs)
- [ ] Implement hybrid search (keyword + semantic)
- [ ] Add CI/CD pipeline

## Contact

For questions about ITNB products and services, visit [itnb.ch](https://www.itnb.ch/en) or use this RAG system to get instant answers!
