from typing import Dict, Any, List


def size_edge(placements: List[Dict[str, Any]], models: Dict[str, Any]) -> Dict[str, Any]:
    num_cams = len(placements)
    model_fps = float(models.get("detector", {}).get("fps", 8))
    total_fps = num_cams * model_fps
    threshold = 120.0  # simple heuristic threshold
    if total_fps < threshold:
        return {"type": "jetson_orin_nx", "gpu_mem_gb": 16, "thermal_ok": True, "total_fps": total_fps}
    return {"type": "ipc_gpu", "gpu_mem_gb": 24, "thermal_ok": True, "total_fps": total_fps}
