# Contributing to BayWalk

## Setup
- Python 3.11+, Node 18+, Docker
- `python -m venv .venv && ./.venv/Scripts/pip install -U pip`
- `cd backend && ../.venv/Scripts/python -m uv pip install -r requirements.in`
- `pre-commit install` (if configured)

## Lint & Type Check
- `ruff check backend`
- `mypy backend/api backend/planners backend/generators`

## Tests
- `cd backend && pytest -q`
- Smoke: `../.venv/Scripts/python backend/scripts/smoke.py`

## PRs
- Branch from `develop`
- Keep commits small, imperative messages
- Fill PR template; include artifacts/links
- CI must pass (tests, SBOM, scan)

## Code Style
- Follow type hints
- Early returns; handle errors; avoid deep nesting
- Document non-obvious behavior in docstrings
