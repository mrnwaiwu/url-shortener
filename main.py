from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, Response
from pydantic import BaseModel, HttpUrl
import redis
import qrcode
import io
import os
import secrets
import string
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="URL Shortener",
    description="Shorten URLs with click tracking and QR code generation, powered by Redis",
    version="2.0.0",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
URL_TTL = int(os.getenv("URL_TTL_SECONDS", "86400"))  # 24 hours
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

r = redis.from_url(REDIS_URL, decode_responses=True)

_ALPHABET = string.ascii_letters + string.digits


def _generate_code(length: int = 6) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = None


@app.get("/")
async def root():
    return {"message": "URL Shortener API v2", "docs": "/docs"}


@app.post("/shorten", status_code=201)
async def shorten_url(req: ShortenRequest):
    """Create a short URL. Optionally supply a custom_code."""
    url_str = str(req.url)

    if req.custom_code:
        code = req.custom_code
        if r.exists(f"url:{code}"):
            raise HTTPException(status_code=409, detail="Custom code already taken")
    else:
        for _ in range(5):
            code = _generate_code()
            if not r.exists(f"url:{code}"):
                break
        else:
            raise HTTPException(status_code=500, detail="Could not generate a unique code")

    pipe = r.pipeline()
    pipe.setex(f"url:{code}", URL_TTL, url_str)
    pipe.setex(f"clicks:{code}", URL_TTL, 0)
    pipe.execute()

    return {
        "short_url": f"{BASE_URL}/{code}",
        "qr_code": f"{BASE_URL}/qr/{code}",
        "code": code,
        "original_url": url_str,
        "expires_in_seconds": URL_TTL,
    }


@app.get("/stats/{code}")
async def get_stats(code: str):
    """Return click count and TTL for a short code."""
    original = r.get(f"url:{code}")
    if not original:
        raise HTTPException(status_code=404, detail="Short URL not found or expired")

    clicks = int(r.get(f"clicks:{code}") or 0)
    ttl = r.ttl(f"url:{code}")

    return {
        "code": code,
        "short_url": f"{BASE_URL}/{code}",
        "qr_code": f"{BASE_URL}/qr/{code}",
        "original_url": original,
        "clicks": clicks,
        "ttl_seconds": ttl,
    }


@app.get("/qr/{code}")
async def get_qr_code(code: str):
    """Generate and return a QR code PNG for the short URL."""
    original = r.get(f"url:{code}")
    if not original:
        raise HTTPException(status_code=404, detail="Short URL not found or expired")

    short_url = f"{BASE_URL}/{code}"

    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    img.add_data(short_url)
    img.make(fit=True)
    pil_img = img.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")


@app.delete("/{code}")
async def delete_url(code: str):
    """Remove a short URL before it expires."""
    if not r.exists(f"url:{code}"):
        raise HTTPException(status_code=404, detail="Short URL not found")
    r.delete(f"url:{code}", f"clicks:{code}")
    return {"message": f"/{code} deleted"}


@app.get("/{code}")
async def redirect(code: str):
    """Redirect to the original URL and increment the click counter."""
    original = r.get(f"url:{code}")
    if not original:
        raise HTTPException(status_code=404, detail="Short URL not found or expired")
    r.incr(f"clicks:{code}")
    return RedirectResponse(url=original, status_code=307)
