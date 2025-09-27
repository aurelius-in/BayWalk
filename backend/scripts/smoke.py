import json, requests, sys

BASE = "http://127.0.0.1:8080"

scene = {
  "scene": {"anchors": [{"type":"bay_rect","width_m":20,"height_m":10}], "zones": [{"name":"lane_A"}]},
  "name": "Bay A",
  "targets": {"num_cameras": 8, "target_fps": 8}
}

print("--- UPLOAD ---", flush=True)
r = requests.post(f"{BASE}/projects/upload", json=scene)
r.raise_for_status()
proj = r.json()
print(json.dumps(proj, indent=2))
pid = proj["id"]

print("\n--- PLAN ---", flush=True)
r = requests.post(f"{BASE}/projects/{pid}/plan")
r.raise_for_status()
print(json.dumps(r.json(), indent=2))

print("\n--- GENERATE ---", flush=True)
r = requests.post(f"{BASE}/projects/{pid}/generate")
r.raise_for_status()
print(json.dumps(r.json(), indent=2))

print("\n--- POLICY ---", flush=True)
r = requests.post(f"{BASE}/projects/{pid}/policy")
r.raise_for_status()
print(json.dumps(r.json(), indent=2))

print("\n--- EVIDENCE ---", flush=True)
r = requests.post(f"{BASE}/projects/{pid}/evidence")
r.raise_for_status()
print(json.dumps(r.json(), indent=2))

print("\n--- METRICS HEAD ---", flush=True)
mm = requests.get(f"{BASE}/metrics").text.splitlines()[:20]
print("\n".join(mm))
