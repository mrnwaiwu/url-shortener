# URL Shortener

A FastAPI URL shortener backed by Redis with click tracking and TTL expiry.

## Features

- Shorten any URL to a random 6-character code
- Optional custom short codes
- Click counter per short URL
- Configurable TTL (links auto-expire)
- Docker Compose setup included

## Quick Start (local)

```bash
# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Clone and install
git clone https://github.com/mrnwaiwu/url-shortener.git
cd url-shortener
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run
uvicorn main:app --reload
```

API docs at `http://localhost:8000/docs`

## Quick Start (Docker Compose)

```bash
cp .env.example .env
docker compose up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/{code}` | Redirect to original URL |
| GET | `/stats/{code}` | Click count and TTL |
| DELETE | `/{code}` | Delete a short URL |

### Shorten a URL

```bash
curl -X POST http://localhost:8000/shorten \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com/very/long/path"}'
```

```json
{
  "short_url": "http://localhost:8000/aB3xYz",
  "code": "aB3xYz",
  "original_url": "https://example.com/very/long/path",
  "expires_in_seconds": 86400
}
```

### Custom code

```bash
curl -X POST http://localhost:8000/shorten \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://github.com/mrnwaiwu", "custom_code": "github"}'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379` | Redis connection string |
| `URL_TTL_SECONDS` | `86400` | Link expiry in seconds (24 h) |
| `BASE_URL` | `http://localhost:8000` | Public base URL for short links |
