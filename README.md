# URL Shortener

A FastAPI URL shortener backed by Redis with click tracking, TTL expiry, and QR code generation.

## Features

- Shorten any URL to a random 6-character code
- Optional custom short codes
- **QR code generation** — returns a PNG for any short link
- Click counter per short URL
- Configurable TTL (links auto-expire)
- Docker Compose setup included

## Quick Start (local)

```bash
docker run -d -p 6379:6379 redis:7-alpine

git clone https://github.com/mrnwaiwu/url-shortener.git
cd url-shortener
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

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
| GET | `/qr/{code}` | Download QR code PNG |
| DELETE | `/{code}` | Delete a short URL |

### Shorten a URL

```bash
curl -X POST http://localhost:8000/shorten \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://github.com/mrnwaiwu"}'
```

```json
{
  "short_url": "http://localhost:8000/aB3xYz",
  "qr_code": "http://localhost:8000/qr/aB3xYz",
  "code": "aB3xYz",
  "original_url": "https://github.com/mrnwaiwu",
  "expires_in_seconds": 86400
}
```

### Get QR code

```bash
curl http://localhost:8000/qr/aB3xYz --output qr.png
```

Or open `http://localhost:8000/qr/aB3xYz` directly in your browser.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379` | Redis connection string |
| `URL_TTL_SECONDS` | `86400` | Link expiry in seconds (24 h) |
| `BASE_URL` | `http://localhost:8000` | Public base URL for short links |
