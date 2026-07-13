# Changelog

## [Unreleased]
- Planned: click analytics per shortened URL
- Planned: expiry TTL option per link
- Planned: user-facing dashboard for link management
- Planned: webhook support for link-click events

## [1.3.2] - 2026-07-13
- Added optional link aliasing via user-provided vanity slugs with conflict detection
- Improved redirect latency by pre-warming slug cache on service startup
- Minor cleanup of slug expiry eviction logic to reduce Redis memory fragmentation

## [1.3.1] - 2026-07-09
- Added configurable slug length via environment variable for shorter or longer codes
- Improved error responses to include a machine-readable error code field
- Minor refactor of the Redis client wrapper to simplify connection retry logic

## [1.3.0] - 2026-07-02
- Added custom domain support allowing shortened links to use user-provided hostnames
- Improved click analytics to include referrer tracking and device-type breakdown
- Minor performance improvements to slug resolution under high concurrency

## [1.2.9] - 2026-06-30
- Added per-link click-count endpoint returning total and unique visitor counts
- Improved slug lookup to return 410 Gone for explicitly deleted links instead of 404
- Minor cleanup of Redis connection pooling configuration for improved reliability

## [1.2.8] - 2026-06-27
- Added audit log endpoint to surface recent shortening and click activity
- Improved slug validation to reject reserved words and common path conflicts
- Minor refactor of redirect handler to reduce middleware latency

## [1.2.7] - 2026-06-27
- Added optional password-protection for shortened links
- Improved redirect performance by caching hot slugs in local memory layer
- Minor refactor of slug generation to improve readability and testability

## [1.2.6] - 2026-06-23
- Added geolocation-based redirect support (optional, opt-in per link)
- Improved slug uniqueness validation to handle concurrent creation requests
- Minor test coverage improvements for the bulk shortening endpoint

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
