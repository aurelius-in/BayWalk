.PHONY: setup up down test lint fmt seed sbom sign cost

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip
	cd backend && uv pip install -r requirements.lock
	cd app && pnpm install

up:
	docker compose up -d

down:
	docker compose down -v

test:
	cd backend && pytest -q

lint:
	cd backend && ruff check .
	cd backend && mypy api planners generators

fmt:
	cd backend && ruff format .

seed:
	cd backend && python scripts/seed_sample_scene.py

sbom:
	syft packages dir:. -o json > sbom.json

sign:
	cosign sign-blob --key ci/keys/cosign.key --output-signature evidence.sig sbom.json

cost:
	cd backend && infracost breakdown --path ../delivery-kit --format table
