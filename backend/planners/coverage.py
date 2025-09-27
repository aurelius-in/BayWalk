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


def _ilp_select_placements(rect: Dict[str, float], n: int) -> List[Dict[str, Any]]:
    # Optional ILP: choose up to n cameras from K candidate positions along the top wall to maximize covered grid cells.
    # Simplified geometry: a cell is covered if within radius r of the camera.
    try:
        from ortools.linear_solver import pywraplp
    except Exception:
        # Fallback to naive if OR-Tools not available
        return _placements_along_wall(rect, n)

    import math
    w, h = rect["w"], rect["h"]
    K = max(n * 4, 8)
    r = 6.0

    # Candidate positions along top wall
    cand: List[Dict[str, float]] = []
    spacing = w / (K + 1)
    for i in range(1, K + 1):
        cand.append({"x": spacing * i, "y": h - 0.5})

    # Grid cells to cover
    gx, gy = 20, 10
    cells = [(w * (ix + 0.5) / gx, h * (iy + 0.5) / gy) for ix in range(gx) for iy in range(gy)]

    # Precompute coverage matrix a[i][j]
    def dist2(ax: float, ay: float, bx: float, by: float) -> float:
        dx, dy = ax - bx, ay - by
        return dx * dx + dy * dy

    a_ij: List[List[int]] = []
    r2 = r * r
    for i, p in enumerate(cand):
        row = []
        for (cx, cy) in cells:
            row.append(1 if dist2(p["x"], p["y"], cx, cy) <= r2 else 0)
        a_ij.append(row)

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        return _placements_along_wall(rect, n)

    x = [solver.BoolVar(f"x_{i}") for i in range(len(cand))]
    y = [solver.BoolVar(f"y_{j}") for j in range(len(cells))]

    # Select exactly n cameras
    solver.Add(solver.Sum(x) == n)

    # Coverage constraints: y_j <= sum_i a_ij x_i
    for j in range(len(cells)):
        solver.Add(y[j] <= solver.Sum(a_ij[i][j] * x[i] for i in range(len(cand))))

    # Objective: maximize covered cells
    solver.Maximize(solver.Sum(y))
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        return _placements_along_wall(rect, n)

    chosen: List[int] = [i for i in range(len(cand)) if x[i].solution_value() > 0.5]
    placements: List[Dict[str, Any]] = []
    for idx, i in enumerate(chosen, start=1):
        p = cand[i]
        placements.append({
            "id": f"cam{idx}",
            "x": round(p["x"], 2),
            "y": round(p["y"], 2),
            "z": 3.0,
            "lens": "2.8mm",
            "fov_deg": 90,
        })
    return placements


def _open3d_placements(rect: Dict[str, float], n: int) -> List[Dict[str, Any]]:
    # Placeholder: later use Open3D to build mesh and sample candidate viewpoints avoiding occlusions
    try:
        import open3d as o3d  # noqa: F401
    except Exception:
        return _placements_along_wall(rect, n)
    # For now, just mirror the wall placement
    return _placements_along_wall(rect, n)


def compute_coverage(scene: Dict[str, Any], targets: Dict[str, Any]) -> Dict[str, Any]:
    rect = _rect_from_anchors(scene)
    n = _num_cams_for_targets(targets)

    use_ilp = bool(targets.get("use_ilp", False))
    use_open3d = bool(targets.get("use_open3d", False))

    if use_open3d:
        placements = _open3d_placements(rect, n)
    elif use_ilp:
        placements = _ilp_select_placements(rect, n)
    else:
        placements = _placements_along_wall(rect, n)

    pct = _naive_coverage_pct(rect, placements)
    blind_spots = 0 if pct > 0.9 else 1
    return {"pct": round(pct, 3), "blind_spots": blind_spots, "placements": placements}
