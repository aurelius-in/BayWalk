from planners.coverage import compute_coverage
from planners.edge_sizing import size_edge
from planners.power_poe import poe_budget


def test_coverage_stub():
    c = compute_coverage({"anchors": []}, {"coverage_pct": 0.9, "num_cameras": 6})
    assert 0 <= c["pct"] <= 1
    assert len(c["placements"]) == 6


def test_edge_sizing_threshold_switch():
    placements = [{"id": f"cam{i}"} for i in range(10)]  # 10 cams
    # model fps 8 -> total 80 < 120 -> jetson
    e1 = size_edge(placements, {"detector": {"fps": 8}})
    assert e1["type"] == "jetson_orin_nx"
    # model fps 16 -> total 160 >= 120 -> ipc_gpu
    e2 = size_edge(placements, {"detector": {"fps": 16}})
    assert e2["type"] == "ipc_gpu"


def test_poe_budget_switch_selection():
    # 30 cams * 12W = 360W < 370 -> 24-port
    placements = [{"id": f"cam{i}", "lens": "2.8mm"} for i in range(30)]
    p1 = poe_budget(placements)
    assert p1["switch"].startswith("PoE+")
    assert p1["switch"] == "PoE+ 24-port"
    # 40 cams ~ 480W -> 48-port
    placements = [{"id": f"cam{i}", "lens": "2.8mm"} for i in range(40)]
    p2 = poe_budget(placements)
    assert p2["switch"] == "PoE+ 48-port"
