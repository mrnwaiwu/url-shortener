# Changelog

## [Unreleased]
- Planned: click analytics per shortened URL
- Planned: expiry TTL option per link

## [1.2.2] - 2026-06-02
- Added configurable redirect response code (301 vs 302) per link
- Improved health check endpoint to include Redis connectivity status
- Minor code cleanup and dependency version bumps

## [1.2.1] - 2026-05-30
- Added slug collision retry logic with configurable max attempts
- Improved validation for custom alias inputs (length, charset)
- Updated docs with curl examples for all endpoints

## [1.2.0] - 2026-05-27
- Added rate limiting middleware to prevent abuse
- Improved error messages for invalid URLs
- Minor performance improvements to Redis lookup

## [1.1.0] - 2026-05-25
- Added QR code generation endpoint

## [1.0.0] - 2026-05-21
- Initial release
- FastAPI URL shortener backed by Redis
- Dockerfile and docker-compose support
