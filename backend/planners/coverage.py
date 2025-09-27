from typing import Dict, Any, List


def _rect_from_anchors(scene: Dict[str, Any]) -> Dict[str, float]:
    # Fallback rectangle: 20m x 10m
    width = 20.0
    height = 10.0
    for a in scene.get("anchors", []):
        if a.get("type") == "bay_rect":
            width = float(a.get("width_m", width))
            height = float(a.get("height_m", height))
    return {"w": width, "h": height}


def _target_fps(targets: Dict[str, Any]) -> float:
    return float(targets.get("target_fps", 8))


def _num_cams_for_targets(targets: Dict[str, Any]) -> int:
    return int(targets.get("num_cameras", 8))


def _placements_along_wall(rect: Dict[str, float], n: int) -> List[Dict[str, Any]]:
    if n <= 0:
        return []
    # Place along the long wall (width)
    w = rect["w"]
    spacing = w / (n + 1)
    placements: List[Dict[str, Any]] = []
    for i in range(1, n + 1):
        x = spacing * i
        y = rect["h"] - 0.5  # near top wall
        placements.append({
            "id": f"cam{i}",
            "x": round(x, 2),
            "y": round(y, 2),
            "z": 3.0,
            "lens": "2.8mm",
            "fov_deg": 90,
        })
    return placements


def _naive_coverage_pct(rect: Dict[str, float], placements: List[Dict[str, Any]]) -> float:
    # Very naive: assume each camera covers a wedge area ~ (fov_deg/360) * pi * r^2
    # Use fixed radius proportional to lens
    if not placements:
        return 0.0
    area_rect = rect["w"] * rect["h"]
    r = 6.0  # meters of useful coverage
    import math
    covered = 0.0
    for p in placements:
        fov = float(p.get("fov_deg", 90))
        covered += (fov / 360.0) * math.pi * r * r
    return max(0.0, min(1.0, covered / area_rect))


def compute_coverage(scene: Dict[str, Any], targets: Dict[str, Any]) -> Dict[str, Any]:
    rect = _rect_from_anchors(scene)
    n = _num_cams_for_targets(targets)
    placements = _placements_along_wall(rect, n)
    pct = _naive_coverage_pct(rect, placements)
    blind_spots = 0 if pct > 0.9 else 1
    return {"pct": round(pct, 3), "blind_spots": blind_spots, "placements": placements}
