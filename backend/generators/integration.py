from pathlib import Path
from typing import List, Dict, Any
import csv


def write_integrations(root: Path, placements: List[Dict[str, Any]]):
    integ = root / "integrations"
    integ.mkdir(parents=True, exist_ok=True)

    # OPC-UA tags CSV
    with (integ / "opcua-tags.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tag", "nodeId", "dataType"])
        for p in placements:
            cam_id = p.get("id")
            writer.writerow([f"cam/{cam_id}/status", f"ns=2;s=cam.{cam_id}.status", "String"])
            writer.writerow([f"cam/{cam_id}/fps", f"ns=2;s=cam.{cam_id}.fps", "Float"])

    # MQTT topics YAML
    import yaml
    topics = {
        "retain": True,
        "topics": [
            {"name": f"cam/{p.get('id')}/events", "qos": 1, "retain": True}
            for p in placements
        ],
    }
    (integ / "mqtt-topics.yaml").write_text(yaml.safe_dump(topics, sort_keys=False))
