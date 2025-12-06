# DFS Web Crawler API

Flask API untuk web crawling menggunakan Depth-First Search algorithm dengan Clean Architecture + Microservice pattern.

## Setup

```bash
python -m venv venv
source venv/bin/activate.fish  # fish shell
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Server: `http://localhost:5000`

## API

### POST /crawl
```bash
curl -X POST http://localhost:5000/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response:**
```json
{
  "start_url": "https://example.com",
  "found_routes": ["/", "/about"],
  "pages_crawled": 2
}
```

### GET /health
```bash
curl http://localhost:5000/health
```

## Config

Environment variables (optional):
```bash
export CRAWLER_TIMEOUT=10
export CRAWLER_MAX_PAGES=100
export CRAWLER_DELAY=0.1
```

## Structure

```
app/
├── container/         # DI Container
├── domain/           # Business entities & interfaces
├── infrastructure/   # External implementations
├── presentation/     # API routes
├── services/         # Business services
└── use_cases/        # Application logic
```

## Stack

- Flask
- requests
- BeautifulSoup4
- Clean Architecture
- Microservice Pattern
- DFS Algorithm (stack-based)
