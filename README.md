# BayWalk

**Walk the bay once. Leave with the BOM, coverage plan, edge sizing, IaC, Jira stories, and a compliance pack.**

BayWalk is a mobile-plus-backend field-architect tool for manufacturing and industrial sites. An on-site “bay walk” becomes deployable artifacts: camera FOV layout with occlusion checks, Jetson vs IPC sizing, PoE and power budgets, hardware BOMs with cost roll-ups, Terraform and Kubernetes manifests, Ignition/OPC-UA tag maps, MQTT topic plans, Jira epics and stories, and a signed compliance bundle. Operates one sprint ahead to unblock delivery teams.

---

## Highlights

- **Scan to Plan:** Capture a quick walkthrough with anchors, export a scene, and generate full planning outputs.
- **Hardware-aware:** Lens selection, mount options, lighting notes, PoE budgets, thermal/power envelopes, and UPS guidance.
- **Edge sizing:** Choose Jetson vs IPC+GPU with throughput math (fps × cams × models), memory and thermal checks.
- **Coverage math:** FOV placement, occlusion detection, and coverage heatmaps with target thresholds.
- **Delivery kit:** Terraform, Helm/K8s, Triton or ONNX Runtime pipeline skeletons, plus MQTT topics and OPC-UA tag CSVs.
- **Agile ready:** Jira epics and stories with DoR/DoD, AC, risks, and spike templates for the next 2–3 sprints.
- **Compliance pack:** Traceability matrix, IQ/OQ/PQ templates, change-control SOP, and signed evidence bundle.

---

## Architecture

```

Mobile (React Native / Expo)
└─ On-device capture (video + anchors) → Scene JSON

Backend (FastAPI, Python)
├─ Scene ingestion and normalization
├─ Planners
│   ├─ Coverage & FOV (Open3D/OpenCV)
│   ├─ PoE & power budgets
│   ├─ Edge sizing (Jetson vs IPC+GPU)
│   └─ Cable route suggestions
├─ Policy gate (OPA) and evidence signer (cosign)
├─ Cost model (Infracost + BOM roll-ups)
└─ Artifact generators
├─ Terraform / Helm / K8s
├─ Ignition/OPC-UA tags, MQTT topics
├─ Jira epics/stories JSON
└─ Compliance bundle (IQ/OQ/PQ, traceability)

Data
├─ Postgres (projects, scenes, BOMs, runs)
└─ MinIO/Azure Blob/S3 (scene and evidence artifacts)

```

**Core libs:** FastAPI, OpenCV, Open3D, OR-Tools, Pydantic, OPA (via REST), Triton or ONNX Runtime, cosign, Infracost.  
**Edge profiles:** Jetson Orin NX/Xavier or Industrial PC + compact GPU.  
**Observability:** OpenTelemetry, Prometheus, Grafana.

---

## Repository Layout

```

BayWalk/
app/                     # React Native (Expo) mobile scanner
backend/
api/                   # FastAPI routers and DTOs
planners/              # coverage, power/PoE, edge sizing, routing
generators/            # terraform, k8s, mqtt, opcua, jira, diagrams
policy/                # OPA policies and tests
compliance/            # IQ/OQ/PQ templates, traceability, SOPs
costs/                 # Infracost integration + BOM rollups
evidence/              # signer, SBOM, provenance
db/                    # migrations, models, seed data
tests/                 # unit/integration tests
delivery-kit/            # emitted IaC and manifests (per project)
docs/
bom/                   # reference BOMs (Jetson vs IPC)
c4/                    # C4 diagrams (context/container/component)
playbooks/             # sprint-ahead spikes, risk matrix, checklists
guides/                # setup, operations, field playbook
jira/                    # epic/story templates + CLI poster
ci/                      # cosign, SBOM, linters, Infracost
README.md

````

---

## Quickstart

### Prerequisites
- Node 18+, Yarn or PNPM, Xcode or Android Studio for the mobile app
- Python 3.11+, Poetry or uv, Docker, Docker Compose
- cosign, opa, terraform, helm, kubectl, Infracost
- Optional: MinIO or cloud blob store for artifacts

### 1) Backend

```bash
cd backend
# create env
cp .env.example .env
# install
poetry install
# run database
docker compose up -d postgres minio
# migrate
poetry run alembic upgrade head
# start API
poetry run uvicorn api.main:app --reload --port 8080
````

### 2) Mobile app

```bash
cd app
cp .env.example .env
# install deps
pnpm install
# run Expo
pnpm expo start
```

### 3) First project from a sample scene

```bash
# seed a sample scene
curl -X POST http://localhost:8080/projects -H "Content-Type: application/json" -d '{
  "name": "Bay A Pilot",
  "targets": {"coverage_pct": 0.9, "latency_ms_p95": 250},
  "scene_ref": "samples/bay-a.scene.json"
}'

# run planners
curl -X POST http://localhost:8080/projects/{project_id}/plan

# generate artifacts
curl -X POST http://localhost:8080/projects/{project_id}/generate
```

Artifacts will be written to `delivery-kit/<project_id>/` and evidence to `backend/evidence/<project_id>/`.

---

## Config

Key environment variables in `backend/.env`:

```
DATABASE_URL=postgresql+psycopg://baywalk:baywalk@localhost:5432/baywalk
ARTIFACT_BUCKET_URL=s3://baywalk-artifacts
ARTIFACT_BUCKET_ENDPOINT=http://localhost:9000
OPA_URL=http://localhost:8181
INFRACOST_API_KEY=...
COSIGN_KEY_PATH=./ci/keys/cosign.key
```

Mobile `app/.env`:

```
API_BASE_URL=http://<your-host>:8080
OFFLINE_CACHE=true
```

---

## Field Workflow

1. **Walk Bay**
   Open the app, select the bay, and record a short walkthrough. Add anchors: ceiling height, bay length, mounting beams. The app exports a `Scene JSON`.

2. **Map Coverage**
   Backend reconstructs rough geometry, suggests candidate mount positions, and projects FOV cones with occlusion flags. Coverage heatmap is computed against target zones.

3. **Place Cams**
   OR-Tools optimizer proposes minimal camera count and lens choices to hit target coverage. User can lock or override placements.

4. **Size Edge**
   Throughput model computes frames per second per camera, model complexity, and streams to propose Jetson vs IPC+GPU with memory and thermal checks.

5. **Route Cables**
   Cable runs, PoE switch tiers, and power budgets are calculated. UPS options and runtime are suggested based on load.

6. **Forge BOM**
   Hardware BOM is assembled with part numbers, vendor hints, unit cost, and total per bay. Cost roll-ups are exported.

7. **Gate Policies**
   OPA evaluates network zones, encryption, RBAC, image signing, and data retention. Results are captured as signed evidence.

8. **Spin Stories**
   Jira epics/stories are generated with DoR/DoD, AC, test notes, and spike templates for the next two sprints.

9. **Print Kits**
   Delivery pack emits Terraform, Helm/K8s, Triton or ONNX Runtime pipelines, Ignition/OPC-UA tag CSVs, MQTT topic maps, and an exec one-pager.

---

## Data Model (abridged)

```json
{
  "project": {
    "id": "uuid",
    "name": "Bay A Pilot",
    "targets": {"coverage_pct": 0.9, "latency_ms_p95": 250},
    "scene_ref": "s3://.../bay-a.scene.json"
  },
  "plan": {
    "coverage": {"pct": 0.93, "blind_spots": 2},
    "placements": [{"id": "cam1", "x": 1.2, "y": 5.6, "z": 3.1, "lens": "2.8mm"}],
    "edge_profile": {"type": "jetson_orin_nx", "gpu_mem_gb": 16},
    "power_poe": {"budget_w": 180, "switch": "PoE+ 24-port"},
    "costs": {"bom_total_usd": 11840.55}
  }
}
```

---

## Planners

* **Coverage & FOV:** Open3D mesh + OpenCV projections. Targets: coverage percent, minimum pixels on target, occlusion threshold.
* **Edge sizing:** FPS × cams × model complexity to GPU/CPU budget. Profiles: Triton (TensorRT) or ONNX Runtime.
* **Power/PoE:** Device draw, PoE class mix, switch tiering, UPS runtime.
* **Routing:** Heuristics for shortest cable runs with mount constraints.

---

## Generated Artifacts

* **IaC:** `delivery-kit/<id>/infra/terraform/` and `helm/` charts for cluster setup, namespaces, RBAC, storage, ingress, and secrets.
* **K8s manifests:** namespace, operators, deployments, configmaps, PVCs.
* **Edge pipelines:** Triton or ONNX Runtime container recipes and configs.
* **Integration:** `opcua-tags.csv`, `mqtt-topics.yaml`, Ignition tag structure.
* **Jira:** `jira/<id>/epics.json`, `stories.json` plus a CLI to post.
* **Compliance:** `compliance/<id>/` with IQ/OQ/PQ templates, traceability matrix, and signed evidence.

---

## Policy Gate

* Identity, RBAC, and network zone checks
* Container image signing and SBOM presence
* Encryption at rest and in transit
* Data retention and redaction rules
* Evidence bundle signed with cosign

Policy results are embedded into the exec read-out and retained in the traceability matrix.

---

## Reference BOMs

Located in `docs/bom/` with two ready profiles:

* **Jetson Orin NX build:** fixed lens cameras, PoE+ switch, M.2 SSD, DIN mount, ventilated enclosure, DC power budget, UPS.
* **IPC + GPU build:** industrial PC, low-profile GPU, PoE switch, NVMe storage, rack or wall mount, UPS.

Each BOM includes part numbers, unit cost, sourcing hints, lens/lighting notes, and installation accessories.

---

## KPIs

* Walk to first deployable plan: under 2 hours
* First-pass coverage: at least 90 percent of target zones
* Estimation error vs actual costs: under 15 percent
* Policy violations caught pre-sprint: over 80 percent
* Stakeholder prep time saved: over 10 hours per bay

---

## Roadmap

* Multi-bay projects and inter-bay cable planning
* Privacy zones and masking with audit
* Thermal imaging support and lighting calculators
* CAD import for higher-fidelity geometry
* Vendor plugin model for cameras, lenses, mounts, and enclosures

---

## Security and Privacy

* Device scans remain local until uploaded by the user.
* All artifacts can be stored in a customer-controlled bucket.
* Evidence bundles use signed digests with SBOMs.
* PII redaction rules available in the policy gate.

---

## Contributing

Issues and PRs are welcome. Please include:

* Problem statement, acceptance criteria, and expected artifacts.
* Planner test cases and sample scenes.
* Policy updates with unit tests.

---

## License

Apache 2.0 (suggested). See `LICENSE`.
