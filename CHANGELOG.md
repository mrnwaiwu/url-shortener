# Changelog

## [Unreleased]
- Planned: click analytics per shortened URL
- Planned: expiry TTL option per link
- Planned: user-facing dashboard for link management
- Planned: webhook support for link-click events

## [1.2.5] - 2026-06-16
- Added structured logging for redirect lookups to aid debugging
- Improved input normalization to strip tracking query parameters on opt-in
- Minor test coverage improvements for slug collision handling

## [1.2.4] - 2026-06-13
- Added bulk URL shortening endpoint accepting JSON array of URLs
- Improved Redis key expiry handling for TTL-based links
- Minor test coverage improvements for edge cases

## [1.2.3] - 2026-06-09
- Added link preview endpoint returning title, description, and OG image metadata
- Improved slug generation to avoid visually ambiguous characters (0/O, l/1)
- Minor documentation updates and test coverage improvements

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
