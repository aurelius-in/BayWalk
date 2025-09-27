from typing import Dict, Any, List


DEFAULT_WATT_PER_CAM = 12.0  # PoE class 0/1 ballpark


def _watt_per_cam(p: Dict[str, Any]) -> float:
    lens = str(p.get("lens", "2.8mm"))
    # Tiny heuristic: varifocal draws a bit more
    if "varifocal" in lens.lower():
        return 14.0
    return DEFAULT_WATT_PER_CAM


def poe_budget(placements: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_watts = sum(_watt_per_cam(p) for p in placements)
    # Choose switch
    if total_watts < 370:
        switch = "PoE+ 24-port"
    else:
        switch = "PoE+ 48-port"
    return {"budget_w": round(total_watts, 1), "switch": switch, "cams": len(placements)}
