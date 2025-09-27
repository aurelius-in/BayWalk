from typing import Dict, Any, List


CATALOG: Dict[str, Dict[str, Any]] = {
    "CAM-2.8MM": {"unit_usd": 350.0, "desc": "2.8mm fixed dome"},
    "JETSON-ORIN-NX": {"unit_usd": 799.0, "desc": "Jetson Orin NX module"},
    "IPC-GPU": {"unit_usd": 1500.0, "desc": "IPC with discrete GPU"},
    "POE24": {"unit_usd": 1200.0, "desc": "PoE+ 24-port switch"},
    "POE48": {"unit_usd": 2200.0, "desc": "PoE+ 48-port switch"},
    "UPS-1500VA": {"unit_usd": 450.0, "desc": "Rack UPS 1500VA"},
    "SSD-2TB": {"unit_usd": 120.0, "desc": "NVMe SSD 2TB"},
    "MOUNTS": {"unit_usd": 25.0, "desc": "Camera wall mounts"},
    "ENCLOSURES": {"unit_usd": 75.0, "desc": "NEMA enclosures"},
    "CABLING-100M": {"unit_usd": 80.0, "desc": "Cat6A bulk 100m"},
    "LABELS": {"unit_usd": 30.0, "desc": "Label pack"},
}


def _item(sku: str, qty: int) -> Dict[str, Any]:
    meta = CATALOG[sku]
    return {"sku": sku, "qty": int(qty), "unit_usd": meta["unit_usd"], "desc": meta["desc"]}


def build_bom(edge: Dict[str, Any], placements: List[Dict[str, Any]]) -> Dict[str, Any]:
    cam_count = len(placements)
    items: List[Dict[str, Any]] = []

    # Cameras and mounts
    items.append(_item("CAM-2.8MM", cam_count))
    items.append(_item("MOUNTS", cam_count))

    # Edge compute
    edge_type = str(edge.get("type", "jetson_orin_nx"))
    if edge_type == "jetson_orin_nx":
        items.append(_item("JETSON-ORIN-NX", 1))
    else:
        items.append(_item("IPC-GPU", 1))

    # Switch selection rough
    if cam_count * 12.0 < 370:
        items.append(_item("POE24", 1))
    else:
        items.append(_item("POE48", 1))

    # Common infra
    items.append(_item("UPS-1500VA", 1))
    items.append(_item("SSD-2TB", 1))
    items.append(_item("ENCLOSURES", 1))
    items.append(_item("CABLING-100M", max(1, round(cam_count / 10))))
    items.append(_item("LABELS", 1))

    total = sum(i["qty"] * float(i["unit_usd"]) for i in items)
    return {"total_usd": round(total, 2), "items": items}
