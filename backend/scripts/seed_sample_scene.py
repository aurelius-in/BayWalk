import json, pathlib
pathlib.Path("samples").mkdir(exist_ok=True)
scene = {"anchors":[{"type":"ceiling_height","m":3.5}],"zones":[{"name":"lane_A"}]}
pathlib.Path("samples/bay-a.scene.json").write_text(json.dumps(scene, indent=2))
print("Seeded samples/bay-a.scene.json")
