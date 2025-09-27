# Security Policy

## Supported Versions
- Main and develop branches

## Reporting a Vulnerability
- Email security@yourcompany.com with details and PoC
- Do not open public issues for sensitive findings

## Secrets
- Never commit secrets. Use `.env` locally and GitHub Secrets in CI.

## Dependencies
- SBOM is generated in CI. Grype scan runs on PRs.

## Data Handling
- Scene JSON written to `samples/` for dev only; production should use object storage (MinIO/S3).
