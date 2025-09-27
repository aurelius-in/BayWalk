#!/usr/bin/env bash
set -euo pipefail

# Bring up services
docker compose up -d

# Backend env
cp -n backend/.env.example backend/.env || true

# Seed sample scene
( cd backend && python scripts/seed_sample_scene.py )

# Start API in background if not running
if ! curl -sf http://localhost:8080/docs >/dev/null 2>&1; then
  echo "Starting API..."
  ( cd backend && uvicorn api.main:app --reload --port 8080 ) &
  sleep 2
fi

# Upload scene and capture project id
PID=$(curl -s -X POST http://localhost:8080/projects/upload \
  -H 'Content-Type: application/json' \
  -d '{"scene":{"anchors":[{"type":"bay_rect","width_m":20,"height_m":10}],"zones":[{"name":"lane_A"}]},"name":"Bay A","targets":{"num_cameras":8,"target_fps":8}}' | jq -r .id)

echo "Project: $PID"

# Run planners
curl -s -X POST http://localhost:8080/projects/$PID/plan | jq '.'

# Generate kit
curl -s -X POST http://localhost:8080/projects/$PID/generate | jq '.'

echo "Delivery kit contents:"
ls -R delivery-kit/$PID || true

# Policy gate
curl -s -X POST http://localhost:8080/projects/$PID/policy | jq '.'

# Evidence
curl -s -X POST http://localhost:8080/projects/$PID/evidence | jq '.'

echo "Done."
