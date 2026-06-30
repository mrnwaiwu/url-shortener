# Rate Limiting

The URL shortener includes a configurable rate limiting middleware to prevent abuse of the shortening and redirect endpoints.

## Configuration

Rate limiting is controlled via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_ENABLED` | `true` | Enable or disable rate limiting globally |
| `RATE_LIMIT_SHORTEN_RPM` | `30` | Max shortening requests per minute per IP |
| `RATE_LIMIT_REDIRECT_RPM` | `300` | Max redirect lookups per minute per IP |
| `RATE_LIMIT_BURST` | `10` | Burst allowance above the per-minute limit |
| `RATE_LIMIT_BACKEND` | `redis` | Backend for rate limit counters (`redis` or `memory`) |

## How It Works

The middleware uses a sliding window counter stored in Redis (or in-process memory for single-instance deployments). Each incoming request increments the counter for the client IP. If the counter exceeds the configured threshold within the window, a `429 Too Many Requests` response is returned.

```
Request → Extract client IP → Increment Redis counter → Check threshold
                                                              │
                                      ┌───────────────────────┤
                                      ▼                       ▼
                               429 Too Many              Forward to handler
                               Requests
```

## Response Headers

Accepted requests include rate limit context headers:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 27
X-RateLimit-Reset: 1751308800
```

## Bypassing Rate Limits (Admin)

Requests authenticated with an `Authorization: Bearer <ADMIN_TOKEN>` header bypass rate limiting. Set `ADMIN_TOKEN` in your environment or `.env` file.

## Example: Docker Compose Override

```yaml
environment:
  RATE_LIMIT_SHORTEN_RPM: "60"
  RATE_LIMIT_REDIRECT_RPM: "600"
  RATE_LIMIT_BURST: "20"
```

## Testing Rate Limits

```bash
# Trigger the rate limit on the shorten endpoint
for i in $(seq 1 35); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8000/shorten \
    -H "Content-Type: application/json" \
    -d '{"url": "https://example.com"}'
done
```

Requests 31–35 should return `429`.
