from typing import Dict, Any, List
import math


def _switch_nodes(scene: Dict[str, Any]) -> List[Dict[str, float]]:
    nodes = []
    for a in scene.get("anchors", []):
        if a.get("type") == "switch_node":
            nodes.append({"x": float(a.get("x", 0.0)), "y": float(a.get("y", 0.0))})
    if not nodes:
        nodes = [{"x": 0.0, "y": 0.0}]  # electrical room default corner
    return nodes


def _dist(a: Dict[str, float], b: Dict[str, float]) -> float:
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


def cable_routes(scene: Dict[str, Any], placements: List[Dict[str, Any]]) -> Dict[str, Any]:
    switches = _switch_nodes(scene)
    paths: List[Dict[str, Any]] = []
    total = 0.0
    for p in placements:
        cam = {"x": float(p.get("x", 0.0)), "y": float(p.get("y", 0.0))}
        nearest = min(switches, key=lambda s: _dist(cam, s))
        length = _dist(cam, nearest)
        total += length
        paths.append({"cam_id": p.get("id"), "to": nearest, "length_m": round(length, 2)})
    return {"total_length_m": round(total, 2), "paths": paths}
